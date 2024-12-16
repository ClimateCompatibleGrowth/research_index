from typing import Any, Dict, List

from neo4j import Driver

from app.db.session import connect_to_db
from app.schemas.workstream import WorkstreamBase, WorkstreamModel


class Workstream:
    @connect_to_db
    def get_all(self, db: Driver) -> List[WorkstreamBase]:
        query = """MATCH (p:Workstream)
                OPTIONAL MATCH (a:Author)-[:member_of]->(p)
                RETURN p.id as id, p.name as name, collect(a) as members"""
        records, summary, keys = db.execute_query(query)
        return [x.data() for x in records]

    @connect_to_db
    def get(self, db: Driver, id: str, type) -> Dict[str, Any]:
        pass