from app.db.session import connect_to_db
from neo4j import Driver


class Output:
    @connect_to_db
    def get(self, id: str, db):
        """ """
        query = """MATCH (p:Article)
                   WHERE p.uuid = $uuid
                   OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                   RETURN DISTINCT p as output, collect(DISTINCT c) as countries;"""
        records, summary, keys = db.execute_query(query, uuid=id)
        print(records[0].data())
        results = dict()
        results = records[0].data()["output"]
        results["countries"] = records[0].data()["countries"]

        authors_query = """MATCH (a:Author)-[r:author_of]->(p:Article)
                            WHERE p.uuid = $uuid
                            RETURN a.uuid as uuid, a.first_name as first_name, a.last_name as last_name, a.orcid as orcid;"""
        records, summary, keys = db.execute_query(authors_query, uuid=id)

        results["authors"] = [x.data() for x in records]

        return results


class OutputList:
    @connect_to_db
    def get(self, db):
        """ """
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
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(DISTINCT a) as authors;
        """
        records, summary, keys = db.execute_query(query)
        return [x.data() for x in records]

    @connect_to_db
    def count(self, db: Driver):
        """Returns counts of the result types

        Arguments
        ---------
        db : Driver
        """
        query = """
                MATCH (a:Author)-[b:author_of]->(o:Article)
                RETURN o.result_type as result_type, count(o) as count
                """
        records, summary, keys = db.execute_query(query)
        return {x.data()["result_type"]: x.data()["count"] for x in records}

    @connect_to_db
    def filter_type(self, db: Driver, result_type: str):
        """Returns all outputs with ordered authors filtering on result type

        Arguments
        ---------
        db
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
                       collect(DISTINCT a) as authors;
        """
        records, summary, keys = db.execute_query(query, result_type=result_type)
        articles = [x.data() for x in records]

        return articles
