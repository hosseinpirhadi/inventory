from sqlalchemy import Column, Integer, String
from src.repository.models import BASE

class Product(BASE):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)