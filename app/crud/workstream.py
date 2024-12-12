from typing import Any, Dict

from neo4j import Driver

from app.db.session import connect_to_db


class Workstream:
    @connect_to_db
    def get_all(self, db: Driver) -> Dict[str, Any]:
        query = """MATCH (p:Workstream)
                OPTIONAL MATCH (a:Author)-[:member_of]->(p)
                RETURN p.id as id, p.name as name, collect(a) as members"""
        records, summary, keys = db.execute_query(query)
        return [x.data() for x in records]

    @connect_to_db
    def get(self, id: str, db: Driver) -> Dict[str, Any]:
        query = """MATCH (p:Workstream)
                WHERE p.id = $id
                OPTIONAL MATCH (a:Author)-[:member_of]->(p)
                RETURN p.id as id, p.name as name, collect(a) as members"""
        records, summary, keys = db.execute_query(query, id=id)
        return records[0].data()