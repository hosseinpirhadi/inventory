from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.controller.auth.oauth2 import oauth2_scheme
from src.controller.schema.product import Product as ProductSchema
from src.controller.schema.product import ProductCreate
from src.repository.models import get_db
from src.services.product_service import ProductService

router = APIRouter(tags=['product'])

product_service = ProductService()

@router.get('/product', response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
def get_products(skip=0, limit=100, db: Session = Depends(get_db)):
    return product_service.get_products(db, skip, limit)

@router.get('/product/{product_id}', response_model=ProductSchema, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)

@router.post('/product', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return product_service.create_product(db, product)

@router.delete('/product', status_code=status.HTTP_200_OK)
def delete_product(product: ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return product_service.delete_product(db, product)
