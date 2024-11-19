from typing import Any, Dict, List, Optional, Tuple

from neo4j import Driver

from app.db.session import connect_to_db


class Country:
    @connect_to_db
    def get(
        self, id: str, db: Driver, result_type: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Retrieve country information and its related research outputs.

        Parameters
        ----------
        id : str
            The unique identifier of the country
        db : Driver
            Neo4j database driver instance
        result_type : Optional[str], default=None
            Filter outputs by specific result type if provided

        Returns
        -------
        Tuple[List[Dict[str, Any]], Dict[str, Any]]
            A tuple containing:
            - List[Dict[str, Any]]: List of output dictionaries, each containing:
                * output details
                * associated authors
                * related countries
            - Dict[str, Any]: Country information dictionary
        """
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
            results, summary, keys = db.execute_query(
                query, id=id, result_type=result_type
            )
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
            results, summary, keys = db.execute_query(query, id=id)

        outputs = [x.data() for x in results]
        query = """MATCH (c:Country) WHERE c.id = $id RETURN c as country;"""
        results, summary, keys = db.execute_query(query, id=id)
        country = results[0].data()["country"]
        return outputs, country

    @connect_to_db
    def count(self, id: str, db: Driver) -> Dict[str, int]:
        """Count articles by result type for a specific country.

        Parameters
        ----------
        id : str
            The unique identifier of the country
        db : Driver
            Neo4j database driver instance

        Returns
        -------
        Dict[str, int]
            Dictionary where:
            - keys: result type strings
            - values: count of articles for each result type
        """
        query = """
                MATCH (o:Article)-[:REFERS_TO]->(c:Country)
                WHERE c.id = $id
                RETURN o.result_type as result_type, count(o) as count
                """
        records, summary, keys = db.execute_query(query, id=id)
        return {x.data()["result_type"]: x.data()["count"] for x in records}


class CountryList:
    @connect_to_db
    def get(self, db: Driver) -> List[Dict[str, Any]]:
        """Retrieve all countries that have associated articles.

        Parameters
        ----------
        db : Driver
            Neo4j database driver instance

        Returns
        -------
        List[Dict[str, Any]]
            List of dictionaries, each containing country properties
            from the Neo4j database
        """
        query = """MATCH (c:Country)<-[:REFERS_TO]-(p:Article)
                RETURN DISTINCT c
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]
