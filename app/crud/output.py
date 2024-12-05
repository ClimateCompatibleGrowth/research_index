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

        query = """
                MATCH (o:Article)
                WHERE o.uuid = $uuid
                OPTIONAL MATCH (o)-[:REFERS_TO]->(c:Country)
                CALL
                {
                WITH o
                MATCH (a:Author)-[b:author_of]->(o)
                RETURN a
                ORDER BY b.rank
                }
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(DISTINCT a) as authors

                """
        records, summary, keys = db.execute_query(query,
                                                        uuid=id)
        data = [x.data() for x in records][0]
        package = data['outputs']
        package['authors'] = data['authors']
        package['countries'] = data['countries']

        return package


    @connect_to_db
    def get_all(self, skip: int, limit: int, db: Driver) -> List[Dict[str, Any]]:
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
                RETURN o as outputs, collect(DISTINCT c) as countries, collect(DISTINCT a) as authors
                SKIP $skip
                LIMIT $limit;
        """
        records, summary, keys = db.execute_query(query,
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
        if len(records) > 0:
            counts = {x.data()["result_type"]: x.data()["count"] for x in records}
            counts['total'] = sum(counts.values())
            return counts
        else:
            return {'total': 0,
                    'publications': 0,
                    'datasets': 0,
                    'other': 0,
                    'software': 0}

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
                       collect(DISTINCT a) as authors
                SKIP $skip
                LIMIT $limit;
        """
        records, _, _ = db.execute_query(query,
                                               result_type=result_type,
                                               skip=skip,
                                               limit=limit)
        return [x.data() for x in records]
