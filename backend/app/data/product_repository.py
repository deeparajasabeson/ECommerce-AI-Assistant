"""
Repository for product catalogue queries.
"""
from app.data._base import BaseRepository

class ProductRepository(BaseRepository):
    def get(self, product_id: str) -> dict | None:
        """
        Fetch a single product by its ID.
        Returns None when not found.
        """
        with self._cur() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
        return self._row(row) if row else None

    def get_all(
            self, 
            *,
            category: str | None = None,
            in_stock: bool | None = None,
            limit: int = 10
    ) -> list[dict]:
        """
        Return products with optional category / stock filters, ordered by ID.
        """
        clauses: list[str] = []
        params: list = []

        if category:
            clauses.append("LOWER(category) = LOWER(%s)")
            params.append(category)
        if in_stock is not None:
            clauses.append("in_stock = %s")
            params.append(in_stock)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(limit)

        with self._cur() as cur:
            cur.execute(
                f"SELECT * FROM products {where} ORDER BY id LIMIT %s", params
            )
            return [self._row(r) for r in cur.fetchall()]

    def search(self, query: str, *, category: str | None = None) -> list[dict]:
        """
        Case-insensitive keyword search across name, description, and category.
        """
        
        q = f"%{query.lower()}%"
        sql = """
            SELECT * FROM products
            WHERE (LOWER(name) LIKE %s OR LOWER(description) LIKE %s OR LOWER(category) LIKE %s)
        """
        params: list = [q, q, q]
        if category:
            sql += " AND LOWER(category) = LOWER(%s)"
            params.append(category)

        with self._cur() as cur:
            cur.execute(sql, params)
            return [self._row(r) for r in cur.fetchall()]
        