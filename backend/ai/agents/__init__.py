"""Agents package for E-Commerce multi-agent system"""
from .product import ProductAgent
from .order import OrderAgent
from .shipping import ShippingAgent
from .customer import CustomerAgent

__all__ = [
    'ProductAgent',
    'OrderAgent',
    'ShippingAgent',
    'CustomerAgent'
]
