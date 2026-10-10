"""
Run once to apply schema and seed data to PostgreSQL database.  
    uv run python init_db.py
"""

from pathlib import Path
import psycopg
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent / "app" / ".env")
DB_DIR = Path(__file__).parent.parent / "db"

conn = psycopg.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
print("Applying Schema...")
cur.execute(DB_DIR / "schema.sql").read_text())

print("Seeding Data...")
cur.execute(DB_DIR / "seed.sql").read_text())
conn.commit()

cur.execute("SELECT COUNT(*) FROM products")
print(f"Number of products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM customers")
print(f"Number of users: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM orders")
print(f"Number of orders: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM shipping_rates")
print(f"Number of shipping rates: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM tracking_events")
print(f"Number of tracking events: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM tracking_info")
print(f"Number of tracking info: {cur.fetchone()[0]}")
print("Database initialization complete.")

cur.close()
conn.close()
print("Done!")
