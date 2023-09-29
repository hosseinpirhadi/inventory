from sqlalchemy.orm import Session
from src.repository.models import Product
from src.controller.schema.product import ProductCreate

class ProductRepository:
    def __init__(self):
        pass

    def get_products(self, db:Session, skip: int, limit: int):
        return db.query(Product).order_by(Product.id).offset(skip).limit(limit).all()

    def get_product_by_id(self, db:Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_product_by_name(self, db:Session, product_name: str):
        return db.query(Product).filter(Product.name == product_name).first()

    def create_product(self, db:Session, product_name: str):
        product = Product(name=product_name)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def delete_product_by_name(self, db:Session, product_name: str):
        product = db.query(Product).filter(Product.name == product_name).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
