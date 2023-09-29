from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.controller.auth.oauth2 import oauth2_scheme
from src.controller.schema.warehouse import Warehouse as WarehouseSchema
from src.controller.schema.warehouse import WarehouseCreate
from src.repository.models import get_db
from src.services.warehouse_service import WarehouseService

router = APIRouter(tags=['warehouse'])

warehouse_service = WarehouseService()

@router.get('/warehouse', response_model=list[WarehouseSchema], status_code=status.HTTP_200_OK)
def get_warehouses(skip=0, limit=100, db: Session = Depends(get_db)):
    return warehouse_service.get_warehouses(db, skip, limit)

@router.get('/warehouse/{warehouse_id}', response_model=WarehouseSchema, status_code=status.HTTP_200_OK)
def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return warehouse_service.get_warehouse_by_id(db, warehouse_id)

@router.post('/warehouse', response_model=WarehouseSchema, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse: WarehouseCreate,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)
                     ):
    return warehouse_service.create_warehouse(db, warehouse)

@router.delete('/warehouse', status_code=status.HTTP_200_OK)
def delete_warehouse(warehous: WarehouseCreate,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)
                    ):
    return warehouse_service.delete_warehouse(db, warehous)