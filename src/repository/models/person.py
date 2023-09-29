from typing import Counter
from sqlalchemy import Column, Integer, String
from src.repository.models import BASE

class Person(BASE):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
