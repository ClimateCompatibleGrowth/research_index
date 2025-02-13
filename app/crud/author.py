from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from fastapi.logger import logger

from neo4j import Driver

from app.db.session import connect_to_db
from app.schemas.author import (AuthorListModel,
                                AuthorOutputModel,
                                AuthorColabModel)
from app.schemas.meta import CountPublication


class Author:

    def get_authors(self,
                    skip: int,
                    limit: int,
                    workstream: list[str] = []) -> AuthorListModel:
        """Get list of authors

        Arguments
        ---------
        skip: int
            Number or records to skip
        limit: int
            Number of records to return

        Returns
        -------
        AuthorListModel

        """
        authors = self.fetch_author_nodes(skip=skip, limit=limit, workstream=workstream)
        if workstream:
            count = len(authors)
        else:
            count = self.count_authors()
        return {"meta": {
                        "count": {"total": count},
                        "skip": skip,
                        "limit": limit},
                "results": authors}

    def get_author(self, id: UUID, result_type: str = 'publication', skip: int = 0, limit: int = 20) -> AuthorOutputModel:
        """Get an author, collaborators and outputs

        Arguments
        ---------
        id: UUID
            Unique author identifier
        result_type: str, default = 'publication',
        skip: int, default = 0
        limit: int, default = 20

        Returns
        -------
        AuthorOutputModel
        """
        if author := self.fetch_author_node(str(id)):
            collaborators = self.fetch_collaborator_nodes(str(id), result_type)[0]
            collaborators = [collaborator.data() for collaborator in collaborators]
            count = self.count_author_outputs(str(id))
            publications = self.fetch_publications(str(id),
                                                   result_type=result_type,
                                                   skip=skip,
                                                   limit=limit)
            author['collaborators'] = collaborators
            author['outputs'] = {'results': publications}
            author['outputs']['meta'] = {"count": count,
                                         "skip": skip,
                                         "limit": limit,
                                         "result_type": result_type}
            return author
        else:
            msg = f"Could not find author with id: {id}"
            logger.error(msg)
            raise KeyError(msg)

    @connect_to_db
    def fetch_author_nodes(
        self, db: Driver, skip: int, limit: int, workstream: List[str] = []
    ) -> List[AuthorColabModel]:
        if workstream:
            query = """
                MATCH (a:Author)-[:member_of]->(u:Workstream)
                WHERE u.id IN $workstream
                OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                RETURN a.first_name as first_name,
                       a.last_name as last_name,
                       a.uuid as uuid,
                       a.orcid as orcid,
                    collect(DISTINCT p) as affiliations, collect(DISTINCT u) as workstreams
                ORDER BY last_name
                SKIP $skip
                LIMIT $limit;"""
        else:
            query = """
                MATCH (a:Author)
                OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
                OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
                RETURN a.first_name as first_name,
                       a.last_name as last_name,
                       a.uuid as uuid,
                       a.orcid as orcid,
                    collect(DISTINCT p) as affiliations, collect(DISTINCT u) as workstreams
                ORDER BY last_name
                SKIP $skip
                LIMIT $limit;"""
        records, _, _ = db.execute_query(query, skip=skip, limit=limit, workstream=workstream)
        return [record.data() for record in records]

    @connect_to_db
    def count_authors(self, db: Driver) -> int:
        """Count the number of authors"""
        query = """MATCH (a:Author)
                RETURN COUNT(a) as count
                """
        records, _, _ = db.execute_query(query)

        return [record.data() for record in records][0]["count"]



    @connect_to_db
    def fetch_author_node(self, id: str, db: Driver) -> Dict[str, Any]:
        author_query = """
            MATCH (a:Author)
            WHERE a.uuid = $uuid
            OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
            OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
            RETURN a.uuid as uuid, a.orcid as orcid,
                    a.first_name as first_name, a.last_name as last_name,
                    collect(DISTINCT p) as affiliations,
                    collect(DISTINCT u) as workstreams;"""
        records, _, _ = db.execute_query(author_query, uuid=id)
        if len(records) == 0:
            return None
        else:
            return records[0].data()

    @connect_to_db
    def count_author_outputs(self, id: str, db: Driver) -> CountPublication:
        query = """
                MATCH (a:Author)-[b:author_of]->(o:Output)
                WHERE (a.uuid) = $uuid
                RETURN o.result_type as result_type, count(DISTINCT o) as count
                """
        records, _, _ = db.execute_query(query, uuid=id)
        if len(records) < 1:
            return {
                "total": 0,
                "publication": 0,
                "dataset": 0,
                "other": 0,
                "software": 0,
            }
        counts = {x.data()["result_type"]: x.data()["count"] for x in records}
        counts["total"] = sum(counts.values())
        return CountPublication(**counts)

    @connect_to_db
    def fetch_collaborator_nodes(
        self, id: str, result_type: str, db: Driver
    ) -> List[Dict[str, Any]]:
        collab_query = """
            MATCH (a:Author)-[:author_of]->(z:Output)<-[:author_of]-(b:Author)
            WHERE a.uuid = $uuid AND b.uuid <> $uuid AND z.result_type = $result_type
            RETURN DISTINCT b.uuid as uuid,
                   b.first_name as first_name,
                   b.last_name as last_name,
                   b.orcid as orcid,
                   count(z) as num_colabs
            ORDER BY num_colabs DESCENDING
            LIMIT 5"""
        return db.execute_query(collab_query, uuid=id, result_type=result_type)

    @connect_to_db
    def fetch_publications(
        self,
        id: str,
        db: Driver,
        result_type: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
    ) -> Tuple:
        if result_type in [
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
                OPTIONAL MATCH (p)-[:refers_to]->(c:Country)
                RETURN p as results,
                       collect(DISTINCT c) as countries,
                       collect(DISTINCT b) as authors
                ORDER BY results.publication_year DESCENDING
                SKIP $skip
                LIMIT $limit
                ;"""

            records, summary, keys = db.execute_query(
                publications_query,
                uuid=id,
                result_type=result_type,
                skip=skip,
                limit=limit,
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
                OPTIONAL MATCH (p)-[:refers_to]->(c:Country)
                RETURN p as results,
                    collect(DISTINCT c) as countries,
                    collect(DISTINCT b) as authors
                ORDER BY results.publication_year DESCENDING
                SKIP $skip
                LIMIT $limit
                ;"""

            records, summary, keys = db.execute_query(
                publications_query, uuid=id, limit=limit, skip=skip
            )
        publications = []

        for record in records:
            data = record.data()
            package = data["results"]
            package["authors"] = data["authors"]
            package["countries"] = data["countries"]
            publications.append(package)

        return publications


