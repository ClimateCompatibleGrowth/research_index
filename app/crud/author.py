from datetime import datetime
from typing import Any, Dict, List, Optional

from neo4j import Driver

from app.db.session import connect_to_db


class Author:
    @connect_to_db
    def get(
        self, id: str, db: Driver,
        result_type: Optional[str] = None,
        limit: int = 20,
        skip: int = 0
    ) -> Dict[str, Any]:
        """Retrieve author information from the database.

        Parameters
        ----------
        id : str
            UUID of the author
        db : Driver
            Neo4j database driver
        result_type : str, optional
            Type of result formatting

        Returns
        -------
        dict
            Author information dictionary containing:
            - uuid : str
                Author's unique identifier
            - orcid : str
                Author's ORCID
            - first_name : str
                Author's first name
            - last_name : str
                Author's last name
            - affiliations : list
                List of partner affiliations
            - workstreams : list
                List of associated workstreams
        Notes
        -----
        Example Neo4j queries:

        MATCH (a:Author)
        RETURN a.first_name as first_name, a.last_name as last_name,
            p.name as affiliation;

        MATCH (a:Author)-[r:author_of]->(p:Article)
        OPTIONAL MATCH (a:Author)-[:member_of]->(p:Partner)
        WHERE a.uuid = $uuid
        RETURN *;
        """
        outputs = []
        author_query = """
            MATCH (a:Author)
            WHERE a.uuid = $uuid
            OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
            OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
            RETURN a.uuid as uuid, a.orcid as orcid,
                    a.first_name as first_name, a.last_name as last_name,
                    collect(p) as affiliations,
                    collect(u) as workstreams;"""

        author, _, _ = db.execute_query(author_query, uuid=id)
        results = author[0].data()

        collab_query = """
            MATCH (a:Author)-[r:author_of]->(p:Output)<-[s:author_of]-(b:Author)
            WHERE a.uuid = $uuid AND b.uuid <> $uuid
            RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid
            LIMIT 5"""
        collab, _, _ = db.execute_query(collab_query, uuid=id)

        results["collaborators"] = [x.data() for x in collab]

        if result_type and result_type in [
            "publication",
            "dataset",
            "software",
            "other",
        ]:
            publications_query = """
                MATCH (a:Author)-[:author_of]->(p:Output)
                WHERE (a.uuid) = $uuid AND (p.result_type = $result_type)
                CALL {
                    WITH p
                    MATCH (b:Author)-[r:author_of]->(p)
                    RETURN b
                    ORDER BY r.rank
                }
                OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                RETURN p as results,
                       collect(DISTINCT c) as countries,
                       collect(DISTINCT b) as authors
                ORDER BY results.publication_year DESCENDING
                SKIP $skip
                LIMIT $limit
                ;"""

            records, _, _ = db.execute_query(
                publications_query,
                uuid=id,
                result_type=result_type,
                skip=skip,
                limit=limit
            )

        else:
            publications_query = """
                MATCH (a:Author)-[:author_of]->(p:Output)
                WHERE a.uuid = $uuid
                CALL {
                    WITH p
                    MATCH (b:Author)-[r:author_of]->(p)
                    RETURN b
                    ORDER BY r.rank
                }
                OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
                RETURN p as results,
                    collect(DISTINCT c) as countries,
                    collect(DISTINCT b) as authors
                ORDER BY results.publication_year DESCENDING
                SKIP $skip
                LIMIT $limit
                ;"""

            records, _, _ = db.execute_query(publications_query,
                                             uuid=id,
                                             limit=limit,
                                             skip=skip)
        for x in records:
            data = x.data()
            package = data['results']
            package['authors'] = data['authors']
            package['countries'] = data['countries']
            outputs.append(package)

        results['outputs'] = {}
        results['outputs']['results'] = outputs
        return results

    @connect_to_db
    def count(self, id: str, db: Driver) -> Dict[str, int]:
        """Returns counts of articles by result type for a given author.

        Parameters
        ----------
        id : str
            UUID of the author
        db : Driver
            Neo4j database driver

        Returns
        -------
        Dict[str, int]
            Dictionary mapping result types to their counts
        """
        query = """
                MATCH (a:Author)-[b:author_of]->(o:Article)
                WHERE (a.uuid) = $uuid
                RETURN o.result_type as result_type, count(DISTINCT o) as count
                """
        records, summary, keys = db.execute_query(query, uuid=id)
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
    def get_all(self, db: Driver, skip: int, limit: int) -> List[Dict[str, Any]]:
        """Retrieve list of authors from the database."""
        query = """MATCH (a:Author)
                   OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                   OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                   RETURN a.first_name as first_name, a.last_name as last_name, a.uuid as uuid, a.orcid as orcid, collect(p) as affiliations, collect(u) as workstreams
                   ORDER BY last_name
                   SKIP $skip
                   LIMIT $limit;
                   """
        records, summary, keys = db.execute_query(query,
                                                  skip=skip,
                                                  limit=limit)

        return [record.data() for record in records]

    @connect_to_db
    def count_authors(self, db: Driver) -> int:
        """Count the number of authors"""
        query = """MATCH (a:Author)
                RETURN COUNT(a) as count
                """
        records, _, _ = db.execute_query(query)

        return [record.data() for record in records][0]['count']