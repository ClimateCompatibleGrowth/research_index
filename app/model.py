from neo4j import GraphDatabase, Driver
import os
from functools import wraps

MG_HOST = os.environ.get('MG_HOST', '127.0.0.1')
MG_PORT = int(os.environ.get('MG_PORT', 7687))

print(f"Host is {MG_HOST} and port is {MG_PORT}")


def connect_to_db(f):
    @wraps(f)
    def with_connection_(*args, **kwargs):

        try:
            URI = f"bolt://{MG_HOST}:{MG_PORT}"
            AUTH = ("", "")
            with GraphDatabase.driver(URI, auth=AUTH) as db:
                db.verify_connectivity()
                result = f(*args, db, **kwargs)
        except Exception as e:
            raise ValueError(e)
        finally:
            db.close()
        return result
    return with_connection_


class OutputList:

    @connect_to_db
    def get(self, db):
        """
        """
        query = """
                MATCH (o:Article)
                OPTIONAL MATCH (o)-[:REFERS_TO]->(c:Country)
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(a) as authors;
        """
        records, summary, keys = db.execute_query(query)
        articles = [x.data() for x in records]

        return articles

    @connect_to_db
    def filter_type(self, db: Driver, result_type: str):
        """Returns all outputs with ordered authors filtering on result type

        Arguments
        ---------
        dbL
        result_type: str
        """
        query = """
                MATCH (o:Article)
                WHERE o.result_type = $result_type
                OPTIONAL MATCH (o)-[:REFERS_TO]->(c:Country)
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }
                RETURN o as outputs,
                       collect(DISTINCT c) as countries,
                       collect(a) as authors;
        """
        records, summary, keys = db.execute_query(query,
                                                  result_type=result_type)
        articles = [x.data() for x in records]

        return articles


class AuthorList:

    @connect_to_db
    def get(self, db):
        """

        Notes
        -----

        """
        query = """MATCH (a:Author)
                   OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                   OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                   RETURN a.first_name as first_name, a.last_name as last_name, a.uuid as uuid, a.orcid as orcid, collect(p.id, p.name) as affiliation, collect(u.id, u.name) as workstreams
                   """
        records, summary, keys = db.execute_query(query)

        return records


class Author:

    @connect_to_db
    def get(self, id, db, type=None):
        """

        Notes
        -----
        MATCH (a:Author)
        RETURN a.first_name as first_name, a.last_name as last_name,
               p.name as affiliation;
        MATCH (a:Author)-[r:author_of]->(p:Article)
        OPTIONAL MATCH (a:Author)-[:member_of]->(p:Partner)
        WHERE a.uuid = $uuid
        RETURN *;

        """
        author_query = """MATCH (a:Author) WHERE a.uuid = $uuid
                          OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                          OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                          RETURN a.uuid as uuid, a.orcid as orcid,
                          a.first_name as first_name, a.last_name as last_name,
                          collect(p.id, p.name) as affiliations,
                          collect(u.id, u.name) as workstreams;
                          """
        author, summary, keys = db.execute_query(author_query, uuid=id)
        results = author[0].data()

        collab_query = """MATCH (a:Author)-[r:author_of]->(p:Output)<-[s:author_of]-(b:Author)
                          WHERE a.uuid = $uuid AND b.uuid <> $uuid
                          RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid
                          LIMIT 5"""
        colabs, summary, keys = db.execute_query(collab_query, uuid=id)

        results['collaborators'] = colabs

        if type and type in ['publication', 'dataset', 'software', 'other']:
            publications_query = """MATCH (a:Author)-[:author_of]->(p:Output)
                                    WHERE (a.uuid) = $uuid AND (p.result_type = $type)
                                    CALL {
                                        WITH p
                                        MATCH (b:Author)-[r:author_of]->(p)
                                        RETURN b
                                        ORDER BY r.rank
                                    }
                                    OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                                    RETURN p as outputs,
                                           collect(DISTINCT c) as countries,
                                           collect(b) as authors
                                    ORDER BY outputs.publication_year DESCENDING;"""
        else:
            publications_query = """MATCH (a:Author)-[:author_of]->(p:Output)
                                    WHERE a.uuid = $uuid
                                    CALL {
                                        WITH p
                                        MATCH (b:Author)-[r:author_of]->(p)
                                        RETURN b
                                        ORDER BY r.rank
                                    }
                                    OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                                    RETURN p as outputs,
                                        collect(DISTINCT c) as countries,
                                        collect(b) as authors
                                    ORDER BY outputs.publication_year DESCENDING;"""
        result, summary, keys = db.execute_query(publications_query,
                                                 uuid=id,
                                                 type=type)
        results['outputs'] = [x.data() for x in result]

        return results


class Output:

    @connect_to_db
    def get(self, id: str, db):
        """
        """
        query = """MATCH (p:Article)
                   WHERE p.uuid = $uuid
                   OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                   RETURN DISTINCT p as output, collect(c) as countries;"""
        records, summary, keys = db.execute_query(query, uuid=id)
        print(records[0].data())
        results = dict()
        results = records[0].data()['output']
        results['countries'] = records[0].data()['countries']

        authors_query = """MATCH (a:Author)-[r:author_of]->(p:Article)
                            WHERE p.uuid = $uuid
                            RETURN a.uuid as uuid, a.first_name as first_name, a.last_name as last_name, a.orcid as orcid;"""
        records, summary, keys = db.execute_query(authors_query, uuid=id)

        results['authors'] = [x.data() for x in records]

        return results


class Nodes:

    @connect_to_db
    def get(self, db):

        query = """MATCH (a:Author)
                RETURN a.uuid as id, 0 as group, a.first_name + " " + a.last_name as name, a.orcid as url
                UNION ALL
                MATCH (b:Article)
                RETURN b.uuid as id, 1 as group, b.title as name, "https://doi.org/" + b.doi as url
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class Edges:

    @connect_to_db
    def get(self, db):

        query = """MATCH (p:Article)<-[author_of]-(a:Author)
                RETURN p.uuid as target, a.uuid as source
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class CountryList:

    @connect_to_db
    def get(self, db: Driver):

        query = """MATCH (c:Country)<-[:REFERS_TO]-(p:Article)
                RETURN DISTINCT c
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class Country:

    @connect_to_db
    def get(self, id: str, db: Driver, result_type=None):

        if result_type:
            query = """
                MATCH (o:Output)-[r:REFERS_TO]->(c:Country)
                MATCH (a:Author)-[:author_of]->(o:Output)
                WHERE c.id = $id AND (o.result_type = $result_type)
                RETURN o as outputs, collect(a) as authors;
                """
            results, _, _ = db.execute_query(query, id=id,
                                             result_type=result_type)
        else:
            query = """
                MATCH (o:Output)-[r:REFERS_TO]->(c:Country)
                MATCH (a:Author)-[:author_of]->(o:Output)
                WHERE c.id = $id
                RETURN o as outputs, collect(a) as authors;
                """
            results, _, _ = db.execute_query(query, id=id,
                                             result_type=result_type)
        outputs = [x.data() for x in results]
        query = """MATCH (c:Country) WHERE c.id = $id RETURN c as country;"""
        results, _, _ = db.execute_query(query, id=id)
        country = results[0].data()['country']
        return outputs, country
