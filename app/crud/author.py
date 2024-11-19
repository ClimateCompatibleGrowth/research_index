from typing import Any, Dict, List, Optional

from neo4j import Driver

from app.db.session import connect_to_db


class Author:
    @connect_to_db
    def get(
        self, id: str, db: Driver, result_type: Optional[str] = None
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
        author_query = """
            MATCH (a:Author) WHERE a.uuid = $uuid
            OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
            OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
            RETURN a.uuid as uuid, a.orcid as orcid,
                    a.first_name as first_name, a.last_name as last_name,
                    collect(p.id, p.name) as affiliations,
                    collect(u.id, u.name) as workstreams;"""

        author, _, _ = db.execute_query(author_query, uuid=id)
        results = author[0].data()

        collab_query = """
            MATCH (a:Author)-[r:author_of]->(p:Output)<-[s:author_of]-(b:Author)
            WHERE a.uuid = $uuid AND b.uuid <> $uuid
            RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid
            LIMIT 5"""
        colabs, summary, keys = db.execute_query(collab_query, uuid=id)

        results["collaborators"] = colabs

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
                RETURN p as outputs,
                       collect(DISTINCT c) as countries,
                       collect(DISTINCT b) as authors
                ORDER BY outputs.publication_year DESCENDING;"""

            result, _, _ = db.execute_query(
                publications_query, uuid=id, result_type=result_type
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
                RETURN p as outputs,
                    collect(DISTINCT c) as countries,
                    collect(DISTINCT b) as authors
                ORDER BY outputs.publication_year DESCENDING;"""

            result, summary, keys = db.execute_query(publications_query, uuid=id)

        results["outputs"] = [x.data() for x in result]

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
                RETURN o.result_type as result_type, count(o) as count
                """
        records, summary, keys = db.execute_query(query, uuid=id)
        return {x.data()["result_type"]: x.data()["count"] for x in records}


class AuthorList:
    """Retrieve list of authors from the database.

    Parameters
    ----------
    db : Driver
        Neo4j database driver

    Returns
    -------
    List[Dict[str, Any]]
        List of author dictionaries containing:
        - first_name : str
        - last_name : str
        - uuid : str
        - orcid : str
        - affiliations : List[Dict[str, str]]
        - workstreams : List[Dict[str, str]]
    """

    @connect_to_db
    def get(self, db: Driver) -> List[Dict[str, Any]]:
        """Retrieve list of authors from the database."""
        query = """MATCH (a:Author)
                   OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                   OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                   RETURN a.first_name as first_name, a.last_name as last_name, a.uuid as uuid, a.orcid as orcid, collect(p.id, p.name) as affiliation, collect(u.id, u.name) as workstreams
                   ORDER BY last_name;
                   """
        records, summary, keys = db.execute_query(query)

        return records
