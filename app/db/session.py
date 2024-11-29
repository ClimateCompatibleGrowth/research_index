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
                result = f(*args, db, **kwargs)
        except Exception as e:
            raise ValueError(e)
        finally:
            db.close()
        return result

    return with_connection_
