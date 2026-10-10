from typing import Optional
from unicodedata import category
from fastapi import APIRouter, HTTPException, Depends, Query
from app.data.product_repository import ProductRepository
from app.data.repositories import get_product_repo

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/search")
def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    repo: ProductRepository = Depends(get_product_repo),
):
    """
    Search products by name, description, or category.
    """
    results = repo.search(q, category=category)
    return{
        "query": q,
        "category": category,
        "count": len(results),
        "results": results
    }

@router.get("")
def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
    limit: int = Query(10, description="Maximum number of results"),
    repo: ProductRepository = Depends(get_product_repo),
):
    """
    List all products with optional filters.
    """
    results = repo.get_all(category=category, 
                           in_stock=in_stock, 
                           limit=limit)
    return{
        "count": len(results),
        "products": results
    }


@router.get("/{product_id}/inventory")
def check_inventory(
    product_id: int,
    repo: ProductRepository = Depends(get_product_repo),
):
    """
    Check inventory availability for a product.
    """
    product = repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "product_id": product_id,
        "product_name": product["name"],
        "in_stock": product["in_stock"],
        "quantity": product["quantity"],
        "availability": "Available" if product["in_stock"] else "Out of Stock",
        "restock_date": None if product["in_stock"] else "2025-01-15"
    }


@router.get("/{product_id}")
def get_product(
    product_id: str,
    repo: ProductRepository = Depends(get_product_repo),
):
    """
    Get detailed information about a specific product.
    """
    product = repo.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
