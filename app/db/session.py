import os
from functools import wraps

from neo4j import GraphDatabase

MG_HOST = os.environ.get("MG_HOST", "127.0.0.1")
MG_PORT = int(os.environ.get("MG_PORT", 7687))

print(f"Host is {MG_HOST} and port is {MG_PORT}")


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
