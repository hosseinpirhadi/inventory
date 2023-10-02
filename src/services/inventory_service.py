from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.controller.schema import InventoryReport
from src.repository.inventory_repository import InventoryRepository
from src.repository.models import get_db
from src.repository.person_repository import PersonRepository
from src.repository.product_count_repository import ProductCountRepository
from src.repository.product_repository import ProductRepository
from src.repository.warehouse_repository import WarehouseRepository
from src.services.helper_functions import (string_to_time_foramt,
                                           time_format_to_string)


class InventoryService:
    def __init__(self):
        self.repository = InventoryRepository()

    def get_inventory_by_date_range(self, db:Session, skip: int, limit: int, start_time: Optional[str] = None, end_time: Optional[str] = None):
        if start_time:
            start_time = string_to_time_foramt(start_time)

        if end_time:
            end_time = string_to_time_foramt(end_time)

        if start_time and end_time:
            if start_time > end_time:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='start time must be less than end time.')

        return self.repository.get_inventory_by_date_range(db, start_time, end_time, skip, limit)

    def get_inventory_report(self, db:Session, skip: int, limit: int, start_time: Optional[str] = None, end_time: Optional[str] = None):

        if start_time:
            start_time = string_to_time_foramt(start_time)
        if end_time:
            end_time = string_to_time_foramt(end_time)

        if start_time and end_time:
            if start_time > end_time:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='start time must be less than end time.')

        results = self.repository.get_inventory_report(db, start_time, end_time, skip, limit)

        inventory_responses = []

        for inventory, receiver, delivery in results:
            inventory_response = InventoryReport(
                id=inventory.id,
                product_id=inventory.product_id,
                ware_house_id=inventory.ware_house_id,
                delivery_person_id=inventory.delivery_person_id,
                receiver_person_id=inventory.receiver_person_id,
                kind=inventory.kind,
                quantity=inventory.quantity,
                created_at=time_format_to_string(inventory.created_at),
                receiver_name=receiver.name,
                delivery_person_name=delivery.name
            )
            inventory_responses.append(inventory_response)
        return inventory_responses

    def insert_inventory(
                            self,
                            db: Session,
                            product_id: int,
                            ware_house_id: int,
                            receiver_id: int,
                            deliver_id: int,
                            kind: bool,
                            quantity: int,
                            datetime: Optional[str] = None
                        ):

        return self._insert_inventory_with_checks(
                                                    db,
                                                    product_id,
                                                    ware_house_id,
                                                    receiver_id,
                                                    deliver_id,
                                                    kind,
                                                    quantity,
                                                    date_time=datetime
                                                )

    def _insert_inventory_with_checks(
        self,
        db: Session,
        product_id: int,
        ware_house_id: int,
        receiver_id: int,
        deliver_id: int,
        kind: bool,
        quantity: int,
        date_time: Optional[datetime]
    ):
        try:
            with db.begin():
                self._check_product_existence(db, product_id)
                self._check_warehouse_existence(db, ware_house_id)
                self._check_product_quantity(db, product_id, ware_house_id, quantity, kind)
                self._check_person_existence(db, receiver_id, "Receiver")
                self._check_person_existence(db, deliver_id, "Delivery")

                create_time = None
                if date_time is not None:
                    create_time = self.string_to_time_foramt(date_time)

                return self.repository.insert_inventory(
                    db,
                    product_id,
                    ware_house_id,
                    receiver_id,
                    deliver_id,
                    kind,
                    quantity,
                    datetime=create_time
                )

        except HTTPException as e:
            raise e
        except Exception as e:
            raise e
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Something went wrong.')
        finally:
            db.rollback()

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

    def _check_product_quantity(self, db: Session, product_id: int, warehouse_id: int, quantity: int, kind: bool):
        productcount_repo = ProductCountRepository()
        productcount = productcount_repo.get_product_amount(db, product_id, ware_house_id=warehouse_id)

        if productcount is None and not kind:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There is no product with ID {product_id} in warehouse with ID {warehouse_id} to be exported.")

        if productcount is None:
            productcount_repo._add_product_amount(db, product_id, warehouse_id, quantity)

        if productcount < quantity and not kind:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Product amount should be more than quantity.")
        else:
            productcount_repo.update_product_amount(db, product_id, warehouse_id, -quantity)

    def _check_person_existence(self, db: Session, person_id: int, person_type: str):
        person = PersonRepository().get_person_by_id(db, person_id)
        if not person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{person_type} person with ID {person_id} does not exist.")
