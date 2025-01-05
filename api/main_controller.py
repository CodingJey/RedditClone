from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infra.database import get_db
from schemas.schemas import ProductCreate, ProductRead
from services.service import (
    create_product_service,
    get_product_service,
    list_products_service,
    update_product_service,
    delete_product_service
)

router = APIRouter()

@router.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_service(db, product)

@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_service(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products/", response_model=list[ProductRead])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_products_service(db, skip, limit)

@router.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    updated_product = update_product_service(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not delete_product_service(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}
