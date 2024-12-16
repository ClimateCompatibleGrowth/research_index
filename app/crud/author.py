from typing import Any, Dict, List, Optional, Tuple

from neo4j import Driver

from app.db.session import connect_to_db
from app.schemas.author import AuthorListModel, AuthorOutputModel


class Author:
    @connect_to_db
    def fetch_author_nodes(
        self, db: Driver, skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        query = """
            MATCH (a:Author)
            OPTIONAL MATCH (a)-[:member_of]->(p:Partner)
            OPTIONAL MATCH (a)-[:member_of]->(u:Workstream)
            RETURN a.first_name as first_name, a.last_name as last_name, a.uuid as uuid, a.orcid as orcid,
                collect(DISTINCT p) as affiliations, collect(DISTINCT u) as workstreams
            ORDER BY last_name
            SKIP $skip
            LIMIT $limit;"""
        return db.execute_query(query, skip=skip, limit=limit)

    @connect_to_db
    def count_authors(self, db: Driver) -> int:
        """Count the number of authors"""
        query = """MATCH (a:Author)
                RETURN COUNT(a) as count
                """
        records, summary, keys = db.execute_query(query)

        return [record.data() for record in records][0]["count"]

    def get_authors(self, skip: int, limit: int) -> AuthorListModel:
        records, summary, keys = self.fetch_author_nodes(skip=skip, limit=limit)
        authors = [record.data() for record in records]
        count = self.count_authors()
        return {"meta": {"count": {"total": count}}, "authors": authors}

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
        records, summary, keys = db.execute_query(author_query, uuid=id)
        return records[0].data()

    @connect_to_db
    def count_author_outputs(self, id: str, db: Driver) -> int:
        query = """
                MATCH (a:Author)-[b:author_of]->(o:Article)
                WHERE (a.uuid) = $uuid
                RETURN o.result_type as result_type, count(DISTINCT o) as count
                """
        records, summary, keys = db.execute_query(query, uuid=id)
        if len(records) <= 0:
            return {
                "total": 0,
                "publications": 0,
                "datasets": 0,
                "other": 0,
                "software": 0,
            }
        counts = {x.data()["result_type"]: x.data()["count"] for x in records}
        counts["total"] = sum(counts.values())
        return counts

    @connect_to_db
    def fetch_collaborator_nodes(
        self, id: str, result_type: str, db: Driver
    ) -> List[Dict[str, Any]]:
        collab_query = """
            MATCH (a:Author)-[:author_of]->(z:Output)<-[:author_of]-(b:Author)
            WHERE a.uuid = $uuid AND b.uuid <> $uuid AND z.result_type = $type
            RETURN DISTINCT b.uuid as uuid,
                   b.first_name as first_name,
                   b.last_name as last_name,
                   b.orcid as orcid,
                   count(z) as num_colabs
            ORDER BY num_colabs DESCENDING
            LIMIT 5"""
        return db.execute_query(collab_query, uuid=id, type=result_type)

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
                OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
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
                OPTIONAL MATCH (p)-[:REFERS_TO]->(c:Country)
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

    def get_author(self, id: str, type: str = 'publication', skip: int = 0, limit: int = 20) -> AuthorOutputModel:
        author = self.fetch_author_node(id)
        collaborators = self.fetch_collaborator_nodes(id, type)[0]
        collaborators = [collaborator.data() for collaborator in collaborators]
        count = self.count_author_outputs(id)
        publications = self.fetch_publications(id, result_type=type, skip=skip, limit=limit)
        author['collaborators'] = collaborators
        author['outputs'] = {'results': publications}
        author['outputs']['meta'] = {"count":count,
                                    "db_response_time_ms": 0,
                                    "page": 0,
                                    "per_page": 0}
        return author