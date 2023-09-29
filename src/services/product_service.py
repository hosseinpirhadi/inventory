from fastapi import HTTPException, status
from src.controller.schema.product import ProductCreate
from src.repository.product_repository import ProductRepository
from sqlalchemy.orm import Session

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_products(self, db: Session, skip: int, limit: int):
        return self.repository.get_products(db, skip, limit)

    def get_product_by_id(self, db: Session, product_id: int):
        product = self.repository.get_product_by_id(db, product_id)
        if product:
            return product
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no product with id: {product_id}')

    def create_product(self, db: Session, product: ProductCreate):
        db_product = self.repository.get_product_by_name(db, product.name.strip().lower())
        if db_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Product with name: {product.name} already exists')
        return self.repository.create_product(db, product.name.strip().lower())

    def delete_product(self, db: Session, product: ProductCreate):
        is_deleted = self.repository.delete_product_by_name(db, product.name.strip().lower())
        if is_deleted:
            return {"message": f"Product {product.name} has been deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no product with name {product.name}')
