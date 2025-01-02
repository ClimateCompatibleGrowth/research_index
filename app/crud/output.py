from typing import Any, Dict, List
from uuid import UUID
from neo4j import Driver
from fastapi.logger import logger

from app.db.session import connect_to_db
from app.schemas.output import OutputListModel, OutputModel


class Output:
    @connect_to_db
    def get_output(self, id: UUID, db: Driver) -> OutputModel:
        """Retrieve article output information from the database.

        Parameters
        ----------
        id : str
            UUID of the article
        db : Driver
            Neo4j database driver

        Returns
        -------
        Dict[str, Any]
            Article output information containing:
            - Article properties from Neo4j
            - countries : List[Dict]
                List of countries referenced in the article
            - authors : List[Dict]
                List of author dictionaries containing:
                - uuid : str
                    Author's unique identifier
                - first_name : str
                    Author's first name
                - last_name : str
                    Author's last name
                - orcid : str
                    Author's ORCID identifier
        """

        query = """
                MATCH (o:Output)
                WHERE o.uuid = $uuid
                OPTIONAL MATCH (o)-[:refers_to]->(c:Country)
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(DISTINCT a) as authors
                """
        records, _, _ = db.execute_query(query, uuid=str(id))
        if records:
            data = [x.data() for x in records][0]
            package = data['outputs']
            package['authors'] = data['authors']
            package['countries'] = data['countries']

            return package
        else:
            logger.error(f"Output {str(id)} does not exist in database")
            raise KeyError(f"Output {str(id)} does not exist")

    @connect_to_db
    def count(self, db: Driver) -> Dict[str, int]:
        """Count articles by result type.

        Parameters
        ----------
        db : Driver
            Neo4j database driver

        Returns
        -------
        Dict[str, int]
            Dictionary mapping result types to their counts
            Example: {'journal_article': 5, 'conference_paper': 3}
        """
        query = """
                MATCH (a:Author)-[b:author_of]->(o:Output)
                RETURN o.result_type as result_type, count(DISTINCT o) as count
                """
        records, _, _ = db.execute_query(query)
        if len(records) <= 0:
            return {'total': 0,
                    'publication': 0,
                    'dataset': 0,
                    'other': 0,
                    'software': 0}
        counts = {x.data()["result_type"]: x.data()["count"] for x in records}
        counts['total'] = sum(counts.values())
        return counts

    @connect_to_db
    def filter_type(self, db: Driver, result_type: str, skip: int, limit: int) -> List[Dict[str, Any]]:
        """Filter articles by result type and return with ordered authors.

        Parameters
        ----------
        db : Driver
            Neo4j database driver
        result_type : str
            Type of result to filter by (e.g. 'journal_article')

        Returns
        -------
        List[Dict[str, Any]]
            Filtered list of articles containing:
            - outputs : Dict
                Article properties
            - countries : List[Dict]
                List of referenced countries
            - authors : List[Dict]
                List of authors ordered by rank

        Raises
        ------
        ValueError
            If result_type is invalid
        """
        query = """
                MATCH (o:Output)
                WHERE o.result_type = $result_type
                OPTIONAL MATCH (o)-[:refers_to]->(c:Country)
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }

                RETURN o as outputs,
                       collect(DISTINCT c) as countries,
                       collect(DISTINCT a) as authors
                SKIP $skip
                LIMIT $limit;
        """
        records, _, _ = db.execute_query(query,
                                         result_type=result_type,
                                         skip=skip,
                                         limit=limit)
        outputs = []
        for x in records:
            data = x.data()
            package = data['outputs']
            package['authors'] = data['authors']
            package['countries'] = data['countries']
            outputs.append(package)

        return outputs

    @connect_to_db
    def filter_country(self,
                       db: Driver,
                       result_type: str,
                       skip: int,
                       limit: int,
                       country: str) -> List[Dict[str, Any]]:
        """Filter articles by country and result type and return with ordered authors.

        Parameters
        ----------
        db : Driver
            Neo4j database driver
        result_type : str
            Type of result to filter by (e.g. 'journal_article')
        skip: int
            Number of rows in the output to skip
        limit: int
            Number of rows to return
        country: str
            Three letter ISO country code

        Returns
        -------
        List[Dict[str, Any]]
            Filtered list of articles containing:
            - outputs : Dict
                Article properties
            - countries : List[Dict]
                List of referenced countries
            - authors : List[Dict]
                List of authors ordered by rank

        Raises
        ------
        ValueError
            If result_type is invalid
        """
        query = """
                MATCH (o:Output)-[:refers_to]->(c:Country)
                WHERE o.result_type = $result_type
                AND c.id = $country_id
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }
                RETURN o as outputs,
                       collect(DISTINCT c) as countries,
                       collect(DISTINCT a) as authors
                SKIP $skip
                LIMIT $limit;
        """
        records, summary, keys = db.execute_query(query,
                                         result_type=result_type,
                                         country_id=country,
                                         skip=skip,
                                         limit=limit)
        outputs = []
        for x in records:
            data = x.data()
            package = data['outputs']
            package['authors'] = data['authors']
            package['countries'] = data['countries']
            outputs.append(package)

        return outputs

    def get_outputs(self,
                    skip: int = 0,
                    limit: int = 20,
                    result_type: str = 'publication',
                    country: str = None) -> OutputListModel:
        """Return a list of outputs"""
        try:
            if country:
                results = self.filter_country(
                    result_type=result_type, skip=skip, limit=limit, country=country
                )
            else:
                results = self.filter_type(result_type=result_type,
                                           skip=skip,
                                           limit=limit)

            count = self.count()

            return {
                "meta": {
                    "count": count,
                    "skip": skip,
                    "limit": limit,
                    "result_type": result_type
                },
                "results": results,
            }
        except ValueError as e:
            raise ValueError(str(e)) from e