from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.controller.auth.oauth2 import oauth2_scheme
from typing import Union
from src.controller.schema.product_count import (ProductCount,
                                                 ProductCountCreate,
                                                 ProductCountReport)
from src.repository.models import get_db
from src.services.product_count_service import ProductCountService

router = APIRouter(tags=['product_count'])

product_count_service = ProductCountService()

@router.get('/productcount/warehouse', response_model=list[ProductCount], status_code=status.HTTP_200_OK)
def get_products_by_warehouse_id(warehouse_id: int = Query(..., description="Warehouse ID"),
                                  skip: int = Query(0, description="Skip records"),
                                  limit: int = Query(100, description="Limit the number of records"),
                                  db: Session = Depends(get_db)):

    return product_count_service.get_products_by_warehouse_id(db, warehouse_id, skip, limit)

@router.get('/productcount/report', response_model=list[ProductCountReport], status_code=status.HTTP_200_OK)
def get_warehouse_report(warehouse_id: int = Query(..., description="Warehouse ID"),
                        skip: int = Query(0, description="Skip records"),
                        limit: int = Query(100, description="Limit the number of records"),
                        db: Session = Depends(get_db)):

    return product_count_service.get_warehouse_report(db, warehouse_id, skip, limit)


@router.get('/productcount/product', response_model=list[ProductCount], status_code=status.HTTP_200_OK)
def get_warehouses_by_product_id(product_id: int = Query(..., description="Product ID"),
                                 skip: int = Query(0, description="Skip records"),
                                 limit: int = Query(100, description="Limit the number of records"),
                                 db: Session = Depends(get_db)):

    return product_count_service.get_warehouses_by_product_id(db, product_id, skip, limit)

@router.get('/productcount', response_model=Union[ProductCount, dict], status_code=status.HTTP_200_OK)
def get_product_by_product_id_and_warehouse_id(product_id: int = Query(..., description="Product ID"),
                                               warehouse_id: int = Query(..., description="Warehouse ID"),
                                               db: Session = Depends(get_db)):

    return product_count_service.get_product_by_product_id_and_warehouse_id(db,
                                                                            product_id,
                                                                            warehouse_id)

@router.post('/productcount', response_model=ProductCountCreate, status_code=status.HTTP_201_CREATED)
def add_product_amount(product_count_create: ProductCountCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    return product_count_service.add_product_amount(db,
                                                product_count_create.product_id,
                                                product_count_create.ware_house_id,
                                                product_count_create.amount
                                            )

@router.get('/productcount/amount', response_model=int, status_code=status.HTTP_200_OK)
def get_product_amount(product_id: int = Query(..., description="Product ID"),
                       warehouse_id: int = Query(..., description="Warehouse ID"),
                       db: Session = Depends(get_db)):

    return product_count_service.get_product_amount(db, product_id, warehouse_id)

@router.put('/productcount', response_model=ProductCountCreate, status_code=status.HTTP_200_OK)
def update_product_amount(product_count_create: ProductCountCreate,
                          db: Session = Depends(get_db),
                          token: str = Depends(oauth2_scheme)):

    return product_count_service.update_product_amount(db,
                                                       product_count_create.product_id,
                                                       product_count_create.ware_house_id,
                                                       product_count_create.amount
                                                    )
