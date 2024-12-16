from typing import Any, Dict, List

from neo4j import Driver

from app.db.session import connect_to_db
from .output import Output


class Country:
    @connect_to_db
    def fetch_country_node(self, id: str, db: Driver) -> Dict[str, Any]:
        """Retrieve country information

        Parameters
        ----------
        id : str
            The unique identifier of the country
        db : Driver
            Neo4j database driver instance


        Returns
        -------
        Dict[str, Any]
            Country information dictionary
        """
        query = """MATCH (c:Country) WHERE c.id = $id RETURN c as country;"""
        results, summary, keys = db.execute_query(query, id=id)
        return results[0].data()["country"]

    @connect_to_db
    def count_country_outputs(self, id: str, db: Driver) -> Dict[str, int]:
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

    @connect_to_db
    def get_countries(self, db: Driver) -> List[Dict[str, Any]]:
        """Retrieve all countries that have associated articles.

        Parameters
        ----------
        db : Driver
            Neo4j database driver instances

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
        return [result.data()["c"] for result in results]

    def get_country(self, id, skip, limit, type) -> Dict[str, Any]:
        entity = self.fetch_country_node(id)
        outputs = Output()
        package = outputs.get_outputs(skip=skip, limit=limit, type=type, country=id)
        package["country"] = entity
        return package
