"""
Repository for shipping rate and shipment tracking queries.
"""
from app.data._base import BaseRepository

class ShippingRepository(BaseRepository):
    """
    Read access to the ''shipping_rates'' and ''tracking_info'', and ''tracking_events'' tables.
    """
    def get_rates(self) -> dict[str, dict]:
        """
        Return all shipping rate tiers keyed by type slug (e.g. ''"standard"''')

        ''_row()'' is applied to each raw DB row before building the result so
                any Decimal cost values are already floats.
        """
        with self._cur() as cur:
            cur.execute("SELECT * FROM shipping_rates ORDER BY cost")
            rows = cur.fetchall()
        return {
            r["type"]: {"name": r["name"], "cost": r["cost"], "days": r["days"]}
            for r in (self._row(row) for row in rows)
        }


    def get_tracking_info(self, tracking_number: str) -> dict | None:
        """
        Fetch tracking info and its full event history for a tracking number.
          
        Returns None when the tracking number does not exist.
        Both queries share the same cursor so they run inside a single
        transaction.  Events are ordered chronologically by insertion ID.
        """
        with self._cur() as cur:
            cur.execute(
                "SELECT * FROM tracking_info WHERE tracking_number = %s",
                (tracking_number,),
            )
            info = cur.fetchone()
            if not info:
                return None

            cur.execute(
                "SELECT * FROM tracking_events WHERE tracking_number = %s ORDER BY id",
                (tracking_number,),
            )
            tracking_events = cur.fetchall()

        return {
            "tracking_number": info["tracking_number"],
            "status": info["status"],
            "current_location": info["current_location"],
            "estimated_delivery": (
                info["estimated_delivery"].strftime("%Y-%m-%d") 
                if info["estimated_delivery"] 
                else None
            ),
            "history": [
                {
                    "timestamp": ev["event_timestamp"],
                    "location": ev["location"],
                    "status": ev["status"],
                }
                for ev in (self._row(event) for event in tracking_events)
            ],
        }
                    