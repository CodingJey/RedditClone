
from sqlalchemy.orm import Session
from models.models import Product
from schemas.schemas import ProductCreate, ProductRead

def create_product_service(db: Session, product: ProductCreate) -> Product:
    """Create a new product entry in the database."""
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product_service(db: Session, product_id: int) -> Product:
    """Retrieve a single product by its ID."""
    return db.query(Product).filter(Product.id == product_id).first()

def list_products_service(db: Session, skip: int = 0, limit: int = 10) -> list[Product]:
    """Retrieve a list of products with optional pagination."""
    return db.query(Product).offset(skip).limit(limit).all()

def update_product_service(db: Session, product_id: int, product: ProductCreate) -> Product:
    """Update an existing product entry in the database."""
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        return None

    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    
    db.commit()
    db.refresh(existing_product)
    return existing_product

def delete_product_service(db: Session, product_id: int) -> bool:
    """Delete a product entry from the database."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True
