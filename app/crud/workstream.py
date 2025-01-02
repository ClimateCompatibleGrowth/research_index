from typing import Any, Dict, List

from neo4j import Driver

from app.db.session import connect_to_db
from app.schemas.workstream import WorkstreamDetailModel, WorkstreamListModel, WorkstreamBase
from .author import Author
from app.schemas.author import AuthorListModel
from app.schemas.output import OutputListModel
from .output import Output

class Workstream:

    def get_all(self, skip: int = 0, limit: int = 20) -> WorkstreamListModel:
        """Return a list of all workstreams

        Arguments
        ---------
        skip: int, default=0
            number of records to skip
        limit: int, default=20
            number of records to return

        Returns
        -------
        app.schema.workstream.WorkstreamListModel
        """
        return {'results': self.get_workstreams(skip=skip, limit=limit),
                'meta': {'count': {'total': self.count_members()},
                         'skip': skip,
                         'limit': limit}}

    def get(self,
            id: str,
            skip: int = 0,
            limit: int = 20) -> WorkstreamDetailModel:
        """Return a list of members for a workstream

        Arguments
        ---------
        id: str
            id of the workstream
        skip: int, default=0
            number of records to skip
        limit: int, default=20
            number of records to return

        Returns
        -------
        app.schema.workstream.WorkstreamDetailModel

        """
        workstream = self.get_workstream_detail(id)
        if workstream:
            members = self.get_members([id] + workstream.pop('children'),
                                    skip=skip,
                                    limit=limit)  # typing: AuthorListModel
            return workstream | {'members': members}
        else:
            return {'members': {}}

    @connect_to_db
    def get_workstream_detail(self, id: str, db: Driver) -> dict:
        query = """MATCH (p:Workstream)
                WHERE p.id = $id
                OPTIONAL MATCH (p)<-[:unit_of]-(b:Workstream)
                RETURN p.id as id, p.name as name, collect(b.id) as children
                """
        records, _, _ = db.execute_query(query, id=id)
        if records:
            return records[0].data()
        else:
            raise KeyError("No records returned for {id}")

    def get_outputs(self, id: str, skip, limit) -> OutputListModel:
        output = Output()
        return output.get_outputs(skip, limit)

    @connect_to_db
    def get_workstreams(self,
                        db: Driver,
                        skip: int = 0,
                        limit: int = 20
                        ) -> list[WorkstreamBase]:
        query = """MATCH (p:Workstream)-[]-(:Author)
                OPTIONAL MATCH (u:Workstream)<-[:unit_of]-(p)
                RETURN DISTINCT u.id as unit_id, u.name as unit_name, p.id as id, p.name as name
                ORDER BY unit_name, name
                SKIP $skip
                LIMIT $limit"""
        records, _, _ = db.execute_query(query, skip=skip, limit=limit)
        if len(records) == 0:
            raise KeyError("No records returned")
        else:
            return [x.data() for x in records]

    def get_members(self,
                    id: list[str],
                    skip: int = 0,
                    limit: int = 20) -> AuthorListModel:
        author = Author()
        return author.get_authors(skip, limit, id)

    @connect_to_db
    def count_members(self, db: Driver) -> int:
        query = """MATCH (p:Workstream)
                RETURN count(DISTINCT p) as count"""
        records, _, _ = db.execute_query(query)
        return records[0].data()['count']
