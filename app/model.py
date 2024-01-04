from gqlalchemy import Memgraph, match, Node
from gqlalchemy.query_builders.memgraph_query_builder import Operator


db = Memgraph(host='127.0.0.1', port=7687)


class OutputList:

    def get(self):
        """

        Notes
        -----
        MATCH (a:Article)
        RETURN a;
        """
        query = """MATCH (a:Article) RETURN a;"""
        results = list(db.execute_and_fetch(query))
        print(results)
        articles = [x['a'].dict() for x in results]

        return articles


class AuthorList:

    def get(self):
        """

        Notes
        -----

        """
        query = """MATCH (a:Author)
                   OPTIONAL MATCH (a:Author)-[:member_of]->(p:Partner)
                   RETURN a.first_name as first_name, a.last_name as last_name, a.uuid as uuid, a.orcid as orcid, p.name as affiliation
                   ORDER BY a.last_name;"""
        results = list(db.execute_and_fetch(query))
        print(results)
        authors = [x for x in results]

        return authors


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
                          OPTIONAL MATCH (a:Author)-[:member_of]->(p:Partner)
                          RETURN a.uuid as uuid, a.orcid as orcid, a.first_name as first_name, a.last_name as last_name, p.name as affiliation;
                          """
        author = list(db.execute_and_fetch(author_query, parameters={'uuid': id}))[0]

        collab_query = """MATCH (a:Author)-[r:author_of]->(p:Article)<-[s:author_of]-(b:Author)
                          WHERE a.uuid = $uuid AND b.uuid <> $uuid
                          RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid
                          LIMIT 5"""
        colabs = list(db.execute_and_fetch(collab_query, parameters={'uuid': id}))

        author['collaborators'] = colabs

        publications_query = """MATCH (a:Author)-[r:author_of]->(p:Article) WHERE a.uuid = $uuid RETURN DISTINCT p.uuid as uuid, p.title as title;"""
        result = list(db.execute_and_fetch(publications_query, parameters={'uuid': id}))
        print(result)
        author['outputs'] = result

        return author


class Output:

    def get(self, id: str):
        """
        """
        print(id)
        query = """MATCH (p:Article)
                   WHERE p.uuid = $uuid
                   RETURN * LIMIT 1"""
        result = list(db.execute_and_fetch(query, parameters={'uuid': id}))[0]['p'].dict()
        print(result)

        authors_query = """MATCH (a:Author)-[r:author_of]->(p:Article)
                            WHERE p.uuid = $uuid
                            RETURN a.uuid as uuid, a.first_name as first_name, a.last_name as last_name, a.orcid as orcid;"""
        author_result = list(db.execute_and_fetch(authors_query, parameters={'uuid': id}))

        print(author_result)

        result['authors'] = author_result
        return result

