from functools import wraps
from  app.core.config import settings


from neo4j import GraphDatabase

MG_HOST = settings.MG_HOST
MG_PORT = settings.MG_PORT


def connect_to_db(f):
    @wraps(f)
    def with_connection_(*args, **kwargs):

        try:
            URI = f"bolt://{MG_HOST}:{MG_PORT}"
            AUTH = ("", "")
            with GraphDatabase.driver(URI, auth=AUTH) as db:
                db.verify_connectivity()
                return f(*args, db, **kwargs)
        except Exception:
            raise
        finally:
            db.close()

    return with_connection_
