from curses.ascii import HT
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repository.product_count_repository import ProductCountRepository
from src.repository.warehouse_repository import WarehouseRepository
from src.repository.product_repository import ProductRepository
from src.controller.schema.product_count import ProductCountReport

class ProductCountService:
    def __init__(self):
        self.repository = ProductCountRepository()

    def get_warehouse_report(self, db: Session, warehouse_id: int, skip: int, limit: int):
        try:
            self._check_warehouse_existence(db, warehouse_id)
        except HTTPException as http_exception:
            raise http_exception

        results = self.repository.get_warehouse_report(db, warehouse_id, skip, limit)
        warehouse_reports = []

        for product_count, product in results:
            warehouse_report = ProductCountReport(
                id=product_count.id,
                product_id=product_count.product_id,
                product_name=product.name,
                ware_house_id=product_count.ware_house_id,
                amount=product_count.amount,
            )

            warehouse_reports.append(warehouse_report)
        return warehouse_reports

    def get_products_by_warehouse_id(self, db:Session, warehouse_id: int, skip: int, limit: int):
        try:
            self._check_warehouse_existence(db, warehouse_id)
        except HTTPException as httpexception:
            raise httpexception

        return self.repository.get_products_by_warehouse_id(db, warehouse_id, skip, limit)

    def get_product_by_product_id_and_warehouse_id(self, db:Session, product_id: int, warehouse_id: int):
        try:
            self._check_warehouse_existence(db, warehouse_id)
            self._check_product_existence(db, product_id)

        except HTTPException as httpexception:
            raise httpexception

        result = self.repository.get_product_by_product_id_and_warehouse_id(db,
                                                                          product_id,
                                                                          warehouse_id
                                                                          )
        if result:
            return result

        return {"message": "There is no inventory for this product and warehouse."}

    def get_warehouses_by_product_id(self, db:Session, product_id: int, skip: int, limit: int):
        try:
            self._check_product_existence(db, product_id)
        except HTTPException as httpexception:
            raise httpexception
        return self.repository.get_warehouses_by_product_id(db, product_id, skip, limit)

    def add_product_amount(self, db:Session, product_id: int, warehouse_id: int, amount: int):
        if amount < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Amount can not be negative.')

        try:
            self._check_product_existence(db, product_id)
            self._check_warehouse_existence(db, warehouse_id)
            result = self.get_product_by_product_id_and_warehouse_id(db, product_id, warehouse_id)

            if type(result) != dict:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Product with ID {product_id} already exists in warehosue with ID {warehouse_id}")
        except HTTPException as http_exception:
            raise http_exception

        return self.repository.add_product_amount(db, product_id, warehouse_id, amount)

    def get_product_amount(self, db:Session, product_id: int, warehouse_id: int):
        try:
            self._check_product_existence(db, product_id)
            self._check_warehouse_existence(db, warehouse_id)
            result = self.get_product_by_product_id_and_warehouse_id(db, product_id, warehouse_id)
            if type(result) == dict:
                raise HTTPException(detail=f"Product with ID {product_id} already exists in warehosue with ID {warehouse_id}")
        except HTTPException as http_exception:
            raise http_exception

        return self.repository.get_product_amount(db, product_id, warehouse_id)

    def update_product_amount(self, db:Session, product_id: int, warehouse_id: int, additional_amount: int):
        try:
            self._check_product_existence(db, product_id)
            self._check_warehouse_existence(db, warehouse_id)
        except HTTPException as httpexception:
            raise httpexception

        result = self.repository.update_product_amount(
                                                        db,
                                                        product_id,
                                                        warehouse_id,
                                                        additional_amount
                                                    )
        if result:
            return result
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no product with ID:{product_id} in warehouse with ID:{warehouse_id}')

    def _check_product_existence(self, db: Session, product_id: int):
        product = ProductRepository().get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with ID {product_id} does not exist.")

    def _check_warehouse_existence(self, db: Session, warehouse_id: int):
        warehouse = WarehouseRepository().get_warehouse_by_id(db, warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Warehouse with ID {warehouse_id} does not exist.")
