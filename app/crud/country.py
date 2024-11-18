from app.db.session import connect_to_db
from neo4j import Driver


class Country:
    @connect_to_db
    def get(self, id: str, db: Driver, result_type=None):

        if result_type:
            query = """
                MATCH (o:Output)-[:REFERS_TO]->(c:Country)
                WHERE c.id = $id AND (o.result_type = $result_type)
                CALL {
                    WITH o
                    MATCH (a:Author)-[r:author_of]->(o)
                    RETURN a
                    ORDER BY r.rank
                }
                OPTIONAL MATCH (o)-[:REFERS_TO]->(d:Country)
                RETURN o as outputs,
                       collect(DISTINCT a) as authors,
                       collect(DISTINCT d) as countries;
                """
            results, _, _ = db.execute_query(query, id=id, result_type=result_type)
        else:
            query = """
                MATCH (o:Output)-[:REFERS_TO]->(c:Country)
                WHERE c.id = $id
                CALL {
                    WITH o
                    MATCH (a:Author)-[r:author_of]->(o)
                    RETURN a
                    ORDER BY r.rank
                }
                OPTIONAL MATCH (o)-[:REFERS_TO]->(d:Country)
                RETURN o as outputs,
                       collect(DISTINCT a) as authors,
                       collect(DISTINCT d) as countries;
                """
            results, _, _ = db.execute_query(query, id=id, result_type=result_type)
        outputs = [x.data() for x in results]
        query = """MATCH (c:Country) WHERE c.id = $id RETURN c as country;"""
        results, _, _ = db.execute_query(query, id=id)
        country = results[0].data()["country"]
        return outputs, country

    @connect_to_db
    def count(self, id: str, db: Driver):
        """Returns counts of the result types

        Arguments
        ---------
        db : Driver
        """
        query = """
                MATCH (o:Article)-[:REFERS_TO]->(c:Country)
                WHERE c.id = $id
                RETURN o.result_type as result_type, count(o) as count
                """
        records, _, _ = db.execute_query(query, id=id)
        return {x.data()["result_type"]: x.data()["count"] for x in records}


class CountryList:
    @connect_to_db
    def get(self, db: Driver):

        query = """MATCH (c:Country)<-[:REFERS_TO]-(p:Article)
                RETURN DISTINCT c
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]
