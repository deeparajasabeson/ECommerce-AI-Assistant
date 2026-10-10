"""
Shared base class for all repository classes.

Provides the psycopg 3 cursor factory and a Decimal-to-float 
row normaliser so every concrete repository inherits them 
without duplication.
"""

from decimal import Decimal
import psycopg
from psycopg.rows import dict_row

class BaseRepository:
    """ Thin wrapper around a psycopg 3 connection.
    
    All domain repositories inherit from this class.  
    The connection is injected at construction time by the FastAPI 
    dependency defined in '' repositories.py'' - repositories themselves never create or close connections.
    """

    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def _cur(self) -> psycopg.Cursor:
        """Return a dict-row cursor for this connection."""
        return self._conn.cursor(row_factory=dict_row)

    @staticmethod
    def _row(row: dict) -> dict:
        """Coerce any Decimal values to float 
        so the dict is JSON-serializable."""
        return {k: float(v) if isinstance(v, Decimal) else v for k, v in row.items()}
