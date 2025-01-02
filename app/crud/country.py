from typing import Any, Dict
from fastapi.logger import logger

from neo4j import Driver

from app.db.session import connect_to_db
from .output import Output

from app.schemas.country import (CountryList,
                                 CountryNodeModel,
                                 CountryOutputListModel)
from app.schemas.meta import CountPublication


class Country:

    def get_country(self,
                    id: str,
                    skip: int = 0,
                    limit: int = 20,
                    result_type: str = 'publication'
                    ) -> CountryOutputListModel:
        """Return a country

        Arguments
        ---------
        id: str
            Three letter country code
        skip: int = 0
        limit: int = 20
        result_type: str = 'publication'

        Returns
        -------
        schemas.output.CountryOutputListModel
        """
        try:
            entity = self.fetch_country_node(id)
        except KeyError as ex:
            logger.error(
                f"Country outputs not found {id}:{skip}:{limit}:{result_type}")
            ex.add_note(f"Could not find {id} in the db")
            raise KeyError(ex)
        else:
            outputs = Output()
            package = outputs.get_outputs(skip=skip,
                                          limit=limit,
                                          result_type=result_type,
                                          country=id)
            counts = self.count_country_outputs(id)
            package["meta"]["count"] = counts
            return package | entity

    def get_countries(self, skip: int = 0, limit: int = 20) -> CountryList:
        """Get a list of countries

        Arguments
        ---------
        skip: int, default=0
        limit: int, default=20

        Returns
        -------
        schemas.country.CountryList
        """
        results = self.get_country_list(skip=skip, limit=limit)
        count = self.count_countries()
        return {"meta": {"count": {'total': count}, "skip": skip, "limit": limit},
                "results": results}

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
        logger.debug(f"Received {results}")
        if results:
            return results[0].data()["country"]
        else:
            msg = f"No results returned from query for country '{id}'"
            logger.error(msg)
            raise KeyError(msg)

    @connect_to_db
    def count_country_outputs(self, id: str, db: Driver) -> CountPublication:
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
                MATCH (o:Output)-[:refers_to]->(c:Country)
                WHERE c.id = $id
                RETURN o.result_type as result_type, count(DISTINCT o) as count
                """
        records, _, _ = db.execute_query(query, id=id)
        if len(records) <= 0:
            return {'total': 0,
                    'publication': 0,
                    'dataset': 0,
                    'other': 0,
                    'software': 0}
        counts = {x.data()["result_type"]: x.data()["count"] for x in records}
        counts['total'] = sum(counts.values())

        return CountPublication(**counts)

    @connect_to_db
    def count_countries(self, db: Driver) -> int:
        """Count the countries"""
        query = """MATCH (c:Country)<-[:refers_to]-(p:Output)
                   RETURN count(DISTINCT c.id) as count"""
        results, _, _ = db.execute_query(query)
        return results[0].data()['count']

    @connect_to_db
    def get_country_list(self,
                         db: Driver,
                         skip: int = 0,
                         limit: int = 20) -> list[CountryNodeModel]:
        """Retrieve all countries that have associated articles.

        Parameters
        ----------
        db : Driver
            Neo4j database driver instances

        Returns
        -------
        list[schemas.country.CountryNodeModel]
        """
        query = """MATCH (c:Country)<-[:refers_to]-(p:Output)
                RETURN DISTINCT c as country
                SKIP $skip
                LIMIT $limit
                """
        records, _, _ = db.execute_query(query, skip=skip, limit=limit)
        return [result.data()['country'] for result in records]
