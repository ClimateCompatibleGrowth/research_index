from neo4j import GraphDatabase
import os

MG_HOST = os.environ.get('MG_HOST', '127.0.0.1')
MG_PORT = int(os.environ.get('MG_PORT', 7687))

db = GraphDatabase.driver(f"bolt://{MG_HOST}:{MG_PORT}")
db.verify_connectivity()
print(f"Host is {MG_HOST} and port is {MG_PORT}")


class OutputList:

    def get(self):
        """

        Notes
        -----
        MATCH (o:Article)
        OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
        RETURN o, collect(c) as countries;
        """
        query = """
            MATCH (o:Article)
            OPTIONAL MATCH (o)-[:REFERS_TO]->(c:Country)
            RETURN o as output, collect(c) as countries;
        """
        records, summary, keys = db.execute_query(query)
        articles = [x.data() for x in records]

        return articles


class AuthorList:

    def get(self):
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

    def get(self, id):
        """

        Notes
        -----
        MATCH (a:Author)
        RETURN a.first_name as first_name, a.last_name as last_name, p.name as affiliation;

        MATCH (a:Author)-[r:author_of]->(p:Article)
        OPTIONAL MATCH (a:Author)-[:member_of]->(p:Partner)
        WHERE a.uuid = $uuid
        RETURN *;

        """
        author_query = """MATCH (a:Author) WHERE a.uuid = $uuid
                          OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                          OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                          RETURN a.uuid as uuid, a.orcid as orcid, a.first_name as first_name, a.last_name as last_name, collect(p.id, p.name) as affiliations,
                          collect(u.id, u.name) as workstreams;
                          """
        author, summary, keys = db.execute_query(author_query, uuid=id)
        results = author[0].data()

        collab_query = """MATCH (a:Author)-[r:author_of]->(p:Article)<-[s:author_of]-(b:Author)
                          WHERE a.uuid = $uuid AND b.uuid <> $uuid
                          RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid
                          LIMIT 5"""
        colabs, summary, keys = db.execute_query(collab_query, uuid=id)

        results['collaborators'] = colabs

        publications_query = """MATCH (a:Author)-[r:author_of]->(p:Article) WHERE a.uuid = $uuid RETURN DISTINCT p.uuid as uuid, p.title as title;"""
        result, summary, keys = db.execute_query(publications_query, uuid=id)
        results['outputs'] = result

        return results


class Output:

    def get(self, id: str):
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

    def get(self):

        query = """MATCH (a:Author)
                RETURN a.uuid as id, 0 as group, a.first_name + " " + a.last_name as name, a.orcid as url
                UNION ALL
                MATCH (b:Article)
                RETURN b.uuid as id, 1 as group, b.title as name, "https://doi.org/" + b.doi as url
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class Edges:

    def get(self):

        query = """MATCH (p:Article)<-[author_of]-(a:Author)
                RETURN p.uuid as target, a.uuid as source
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]