from app.db.session import connect_to_db


class Nodes:
    @connect_to_db
    def get(self, db):

        query = """MATCH (a:Author)
                RETURN a.uuid as id, 0 as group, a.first_name + " " + a.last_name as name, a.orcid as url
                UNION ALL
                MATCH (b:Article)
                RETURN b.uuid as id, 1 as group, b.title as name, "https://doi.org/" + b.doi as url
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]


class Edges:
    @connect_to_db
    def get(self, db):

        query = """MATCH (p:Article)<-[author_of]-(a:Author)
                RETURN p.uuid as target, a.uuid as source
                """
        results, summary, keys = db.execute_query(query)
        return [x.data() for x in results]
