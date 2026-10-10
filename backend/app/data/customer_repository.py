"""
Repository for customer account queries.
"""

from app.data._base import BaseRepository

class CustomerRepository(BaseRepository):
    """Read and write access to the ''Customers.'' table. """

    def get(self, customer_id: int) -> dict | None:
        """
        Fetch a single customer by ID.  
        Returns None when not found.
        """
        with self._cur() as cur:
            cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            row = cur.fetchone()
        return self._row(row) if row else None

    def update_loyalty_points(self, customer_id: int, new_points: int) -> None:
        """
        Overwrite a customer's loyalty-points balance with the given value.
        """
        with self._cur() as cur:
            cur.execute(
                "UPDATE customers SET loyalty_points = %s WHERE id = %s",
                (new_points, customer_id)
            )
            self._conn.commit()