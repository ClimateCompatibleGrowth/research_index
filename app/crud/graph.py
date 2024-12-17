from typing import Any, Dict, List

from neo4j import Driver

from app.db.session import connect_to_db


class Nodes:
    """Class for retrieving graph nodes representing authors and articles."""

    @connect_to_db
    def get(self, db: Driver) -> List[Dict[str, Any]]:
        """Retrieve all author and article nodes from the database.

        Parameters
        ----------
        db : Driver
            Neo4j database driver

        Returns
        -------
        List[Dict[str, Any]]
            List of node dictionaries containing:
            - id : str
                Node UUID
            - group : int
                Node type (0=Author, 1=Article)
            - name : str
                Display name (full name for authors, title for articles)
            - url : str
                Associated URL (ORCID for authors, DOI for articles)

        Raises
        ------
        Neo4jError
            If database query fails
        """
        query = """MATCH (a:Author)
                RETURN a.uuid as id, 0 as group, a.first_name + " " + a.last_name as name, a.orcid as url
                UNION ALL
                MATCH (b:Output)
                RETURN b.uuid as id, 1 as group, b.title as name, "https://doi.org/" + b.doi as url
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class Edges:
    """Class for retrieving graph edges representing author-article relationships."""

    @connect_to_db
    def get(self, db: Driver) -> List[Dict[str, str]]:
        """Retrieve all author-article relationships from the database.

        Parameters
        ----------
        db : Driver
            Neo4j database driver

        Returns
        -------
        List[Dict[str, str]]
            List of edge dictionaries containing:
            - source : str
                Author node UUID
            - target : str
                Article node UUID

        Raises
        ------
        Neo4jError
            If database query fails
        """
        query = """MATCH (p:Output)<-[author_of]-(a:Author)
                RETURN p.uuid as target, a.uuid as source
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]
