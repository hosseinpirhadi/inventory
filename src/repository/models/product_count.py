from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from src.repository.models import BASE
from src.repository.models.product import Product
from src.repository.models.warehouse import Warehouse

class ProductCount(BASE):
    __tablename__ = "ProductCount"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    ware_house_id = Column(Integer, ForeignKey(Warehouse.id), nullable=False)
    amount = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('product_id', 'ware_house_id', name='UC_ProductWarehouse'),)