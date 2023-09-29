import logging
from datetime import datetime
from typing import Union

from sqlalchemy import and_
from sqlalchemy.orm import Session, aliased

from src.repository.models import Inventory, Person


class InventoryRepository:
    def __init__(self):
        pass

    def get_inventory_by_date_range(self, db:Session, start_time: datetime, end_time: datetime, skip: int, limit: int):

        if start_time and end_time:
            return db.query(Inventory).filter(and_(Inventory.created_at >= start_time, Inventory.created_at <= end_time)).\
            order_by(Inventory.created_at).offset(skip).limit(limit).all()

        if start_time:
            return db.query(Inventory).filter(Inventory.created_at >= start_time).\
            order_by(Inventory.created_at).offset(skip).limit(limit).all()

        if end_time:
            return db.query(Inventory).filter(Inventory.created_at <= end_time).\
            order_by(Inventory.created_at).offset(skip).limit(limit).all()

    def get_inventory_report(self, db: Session, start_time: datetime, end_time: datetime, skip: int, limit: int):

        receiver_person = aliased(Person)
        delivery_person = aliased(Person)

        query = (
            db.query(Inventory, receiver_person, delivery_person)
            .join(receiver_person, Inventory.receiver_person_id == receiver_person.id)
            .join(delivery_person, Inventory.delivery_person_id == delivery_person.id)
        )

        if start_time and end_time:
            query = query.filter(and_(Inventory.created_at >= start_time, Inventory.created_at <= end_time))
        elif start_time:
            query = query.filter(Inventory.created_at >= start_time)
        elif end_time:
            query = query.filter(Inventory.created_at <= end_time)

        query = query.order_by(Inventory.created_at).offset(skip).limit(limit)

        results = query.all()

        return results

    def insert_inventory(self,
                        db,
                        product_id: int,
                        ware_house_id: int,
                        receiver_id: int,
                        deliver_id: int,
                        kind: bool,
                        quantity: int,
                        datetime: Union[datetime, None]=None):

        inventory = Inventory(
                                product_id=product_id,
                                ware_house_id=ware_house_id,
                                delivery_person_id=deliver_id,
                                receiver_person_id=receiver_id,
                                kind=kind,
                                quantity=quantity,
                                created_at=datetime
                            )

        db.add(inventory)
        db.flush()

        return inventory
