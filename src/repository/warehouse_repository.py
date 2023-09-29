from sqlalchemy.orm import Session
from src.repository.models import Warehouse

class WarehouseRepository:
    def __init__(self):
        pass

    def get_warehouses(self, db:Session, skip: int, limit: int):
        return db.query(Warehouse).order_by(Warehouse.id).offset(skip).limit(limit).all()

    def get_warehouse_by_id(self, db:Session, warehouse_id: int):
        return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    def get_warehouse_by_name(self, db:Session, warehouse_name: str):
        return db.query(Warehouse).filter(Warehouse.name == warehouse_name).first()

    def create_warehouse(self, db:Session, warehouse_name: str):
        warehouse = Warehouse(name=warehouse_name)
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse

    def delete_warehouse_by_name(self, db:Session, warehouse_name: str):
        warehouse = db.query(Warehouse).filter(Warehouse.name == warehouse_name).first()
        if warehouse:
            db.delete(warehouse)
            db.commit()
            return True
        return False