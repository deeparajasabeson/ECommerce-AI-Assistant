import os
import threading
from pathlib import Path

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

# Load .env relative to this file so DATABASE_URL is available regardless of
# the working directory uvicorn is launched from.
load_dotenv(Path(__file__).parent / ".env")
_pool: ConnectionPool | None = None

# Guards the double checked look below so the pool is created exactly once
# even under concurrent startup requests.
_lock = threading.Lock()

def get_pool() -> ConnectionPool:
    """"""
    global _pool
    if _pool is None:
        with _lock:
            if _pool is None:
                dsn = os.getenv("DATABASE_URL")
                _pool = ConnectionPool(conninfo=dsn, min_size=1, max_size=10)
    return _pool

def get_db():
    """FastAPI dependency - yields a psycopg 3 connection from the pool.
    
    The pool's connection() context manager automatically commits on a clean
    exit and rolls back on any exception, then returns the connection to the 
    pool - no manual clanup needed in route handlers.
    """

    with get_pool().connection() as conn:
        yield conn
