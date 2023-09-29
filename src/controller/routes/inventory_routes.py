from datetime import datetime
from typing import Optional
from src.controller.auth.oauth2 import oauth2_scheme
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.controller.schema.inventory import (InventoryCreate,
                                             InventoryDateRange,
                                             ReturnInventory,
                                             InventoryReport)
from src.repository.models import get_db
from src.services.inventory_service import InventoryService

router = APIRouter(tags=['inventory'])

inventory_service = InventoryService()

@router.get('/inventory', response_model=list[ReturnInventory], status_code=status.HTTP_200_OK)
def get_inventory_by_date_range(
        start_datetime: Optional[str] = Query(None, description="Start datetime for filtering"),
        end_datetime: Optional[str] = Query(None, description="End datetime for filtering"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
    ):
    datetime_range = InventoryDateRange(start_datetime=start_datetime, end_datetime=end_datetime)

    return inventory_service.get_inventory_by_date_range(db, skip, limit, datetime_range.start_datetime, datetime_range.end_datetime)

@router.get('/inventory/report', response_model=list[InventoryReport], status_code=200)
def get_report(
        start_datetime: Optional[str] = Query(None, description="Start datetime for filtering"),
        end_datetime: Optional[str] = Query(None, description="End datetime for filtering"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
    ):

    datetime_range = InventoryDateRange(start_datetime=start_datetime, end_datetime=end_datetime)

    return inventory_service.get_inventory_report(db, skip, limit, datetime_range.start_datetime, datetime_range.end_datetime)

@router.post('/inventory', response_model=ReturnInventory, status_code=status.HTTP_201_CREATED)
def insert_inventory(inventory_create: InventoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return inventory_service.insert_inventory(
                                                db,
                                                inventory_create.product_id,
                                                inventory_create.ware_house_id,
                                                inventory_create.receiver_person_id,
                                                inventory_create.delivery_person_id,
                                                inventory_create.kind,
                                                inventory_create.quantity,
                                                datetime=inventory_create.created_at
                                            )
