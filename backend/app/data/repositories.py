







import psycopg
from fastapi import Depends

from app.database import get_db
from app.data.customer_repository import CustomerRepository
from app.data.shipping_repository import ShippingRepository
from app.data.order_repository import OrderRepository
from app.data.product_repository import ProductRepository

def get_product_repo(conn: psycopg.Connection = Depends(get_db)) -> ProductRepository:
    """
    Provide a ''ProductRepository'' bound to the request's DB connection.
    """
    return ProductRepository(conn)

def get_customer_repo(conn: psycopg.Connection = Depends(get_db)) -> CustomerRepository:
    """
    Provide a ''CustomerRepository'' bound to the request's DB connection.
    """
    return CustomerRepository(conn)

def get_shipping_repo(conn: psycopg.Connection = Depends(get_db)) -> ShippingRepository:
    """
    Provide a ''ShippingRepository'' bound to the request's DB connection.
    """
    return ShippingRepository(conn)

def get_order_repo(conn: psycopg.Connection = Depends(get_db)) -> OrderRepository:
    """
    Provide a ''OrderRepository'' bound to the request's DB connection.
    """
    return OrderRepository(conn)

def get_customer_repo(conn: psycopg.Connection = Depends(get_db)) -> CustomerRepository:
    """
    Provide a ''CustomerRepository'' bound to the request's DB connection.
    """
    return CustomerRepository(conn)

def get_shipping_repo(conn: psycopg.Connection = Depends(get_db)) -> ShippingRepository:
    """
    Provide a ''ShippingRepository'' bound to the request's DB connection.
    """
    return ShippingRepository(conn)
