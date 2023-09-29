from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.controller.schema.warehouse import WarehouseCreate
from src.repository.warehouse_repository import WarehouseRepository


class WarehouseService:
    def __init__(self):
        self.repository = WarehouseRepository()

    def get_warehouses(self, db: Session, skip: int, limit: int):
        # with get_db() as db:
        return self.repository.get_warehouses(db, skip, limit)

    def get_warehouse_by_id(self, db: Session, warehouse_id: int):
        warehouse = self.repository.get_warehouse_by_id(db, warehouse_id)
        if warehouse:
            return warehouse
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no warehouse with id: {warehouse_id}')

    def create_warehouse(self, db: Session, warehouse: WarehouseCreate):
        db_warehouse = self.repository.get_warehouse_by_name(db, warehouse.name.strip().lower())
        if db_warehouse:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Warehouse with name: {warehouse.name} already exists')
        return self.repository.create_warehouse(db, warehouse.name.strip().lower())

    def delete_warehouse(self, db: Session, warehouse: WarehouseCreate):
        is_deleted = self.repository.delete_warehouse_by_name(db, warehouse.name.strip().lower())
        if is_deleted:
            return {"message": f"Warehouse {warehouse.name} has been deleted"}
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'There is no warehouse with name {warehouse.name}')