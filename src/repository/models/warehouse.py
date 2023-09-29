from sqlalchemy import Column, Integer, String
from src.repository.models import BASE

class Warehouse(BASE):
    __tablename__ = "Warehouse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)