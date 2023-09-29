from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, func
from src.repository.models import BASE
from src.repository.models.product import Product
from src.repository.models.warehouse import Warehouse
from src.repository.models.person import Person

class Inventory(BASE):
    __tablename__ = "Inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    ware_house_id = Column(Integer, ForeignKey(Warehouse.id), nullable=False)
    delivery_person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    receiver_person_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    kind = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())