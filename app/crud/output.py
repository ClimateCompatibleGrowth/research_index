from typing import Any, Dict, List

from neo4j import Driver

from app.db.session import connect_to_db


class Output:
    @connect_to_db
    def get(self, id: str, db: Driver) -> Dict[str, Any]:
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
        query = """MATCH (p:Article)
                   WHERE p.uuid = $uuid
                   OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                   RETURN DISTINCT p as output, collect(DISTINCT c) as countries;"""
        records, summary, keys = db.execute_query(query, uuid=id)
        print(records[0].data())
        results = {}
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
    def get(self, db: Driver) -> List[Dict[str, Any]]:
        """Retrieve all article outputs with their associated countries and authors.

        Parameters
        ----------
        db : Driver
            Neo4j database driver

        Returns
        -------
        List[Dict[str, Any]]
            List of dictionaries containing:
            - outputs : Dict
                Article properties
            - countries : List[Dict]
                List of referenced countries
            - authors : List[Dict]
                List of authors ordered by rank
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
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(DISTINCT a) as authors;
        """
        records, summary, keys = db.execute_query(query)
        return [x.data() for x in records]

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
                MATCH (a:Author)-[b:author_of]->(o:Article)
                RETURN o.result_type as result_type, count(o) as count
                """
        records, summary, keys = db.execute_query(query)
        return {x.data()["result_type"]: x.data()["count"] for x in records}

    @connect_to_db
    def filter_type(self, db: Driver, result_type: str) -> List[Dict[str, Any]]:
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
        return [x.data() for x in records]
