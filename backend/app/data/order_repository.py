"""
Repository for order management queries.
"""

from datetime import datetime
from app.data._base import BaseRepository

class OrderRepository(BaseRepository):
    """
    Read and write access to the ''orders'' and ''order_items'' tables.
    """

    #-----------------------------------------------------
    # Private helpers
    #-----------------------------------------------------

    def _fetch_items(self, order_id: str) -> list[dict]:
        """
        Fetch all line items for a given order, ordered by insertion ID.
        """
        with self._cur() as cur:
            cur.execute(
                "SELECT * FROM order_items WHERE order_id = %s ORDER BY id", (order_id,),
            )
            return [self._row(r) for r in cur.fetchall()]


    @staticmethod
    def _build(order_row: dict, items: list[dict]) -> dict:
        """
        Compose a full order dict from a flat orders row + its line items.
        
        The orders table stores the shipping address as flat columns
        (street, city, ...); this helper nests them back into a 
        ''shipping_address'' sub-dict matching the API response shape.
        ''order_row'' must have already been passed through 
        ''_row()'' so all Decimal values are floats.
        """

        return {
            "id": order_row["id"],
            "customer_id": order_row["customer_id"],
            "total_amount": order_row["total_amount"],
            "status": order_row["status"],
            "tracking_number": order_row["tracking_number"],
            "shipping_address": {
                "street": order_row["street"],
                "city": order_row["city"],
                "state": order_row["state"],
                "zip_code": order_row["zip_code"],
                "country": order_row["country"],
            },
            "items": items,
            "created_at": order_row["created_at"],
            "updated_at": order_row["updated_at"],
        }

    #-----------------------------------------------------
    # Public API
    #-----------------------------------------------------
    def get(self, order_id: str) -> dict | None:
        """
        Fetch a single order with its line items.
        Returns None when not found.
        """
        with self._cur() as cur:
            cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order_row = cur.fetchone()
        if not order_row:
            return None
        return self._build(self._row(row), self._fetch_items(order_id))

    def get_all(
            self,
            *,
            customer_id: str | None = None,
            status: str | None = None,
            limit: int = 10,
    ) -> list[dict]:
        """
        List orders with optional customer / status filters, 
        newest first.
        """
        clauses: list[str] = []
        params: list = []

        if customer_id:
            clauses.append("customer_id = %s")
            params.append(customer_id)
        if status:
            clauses.append("LOWER(status) = LOWER(%s)")
            params.append(status)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(limit)

        with self._cur() as cur:
            cur.execute(
                f"SELECT * FROM orders {where} ORDER BY created_at DESC LIMIT %s",
                params,
            )
            order_rows = [self._row(r) for r in cur.fetchall()]

        return [self._build(row, self._fetch_items(row["id"])) for row in order_rows]

    def create(
            self,
            order_id: str,
            customer_id: str,
            items: list[dict],
            total_amount: float,
            shipping_address: dict,
    ) -> dict:
        """
        Insert a new order and its line items in a single transaction.
        '''_conn.commit()'' is called explicitly so that the 
        re-fetch below always reads fully committed data 
        regardless of when the surrounding ''get_db()'' dependency
        finalises its own commit on response exit.
        """

        now = datetime.now()
        with self._cur() as cur:
            cur.execute(
                """
                INSERT INTO orders
                    (id, customer_id, total_amount, status, tracking_number,
                    street, city, state, zip_code, country, created_at, updated_at)
                VALUES (%s, %s, %s, 'pending', NULL, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    order_id, 
                    customer_id, 
                    total_amount, 
                    shipping_address["street"],
                    shipping_address["city"],
                    shipping_address["state"],
                    shipping_address["zip_code"],
                    shipping_address.get("country", "USA"),
                    now,
                    now,
                ),
            )
            for item in items:
                cur.execute(
                    """
                    INSERT INTO order_items 
                        (order_id, product_id, product_name, quantity, price) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order_id, 
                        item["product_id"], 
                        item["product_name"], 
                        item["quantity"], 
                        item["price"]
                    ),
                )
        # Commit before the re-fetch so get() sees the new rows.    
        self._conn.commit()
        return self.get(order_id)

    def update_status(self, order_id: str, status: str) -> None:
        """
        Update an order's status and bump its updated_at timestamp.
        """
        with self._cur() as cur:
            cur.execute(
                "UPDATE orders SET status = %s, updated_at = %s WHERE id = %s",
                (status, datetime.now(), order_id),
            )
        # Explicit commit so the calling router reads the updated state immediately.
        self._conn.commit()