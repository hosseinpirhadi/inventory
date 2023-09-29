import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
ENGINE = create_engine(CONNECTION_STRING)

SESSION = sessionmaker(bind=ENGINE)
BASE = declarative_base()

def get_db():
    db = SESSION()
    try:
        yield db
    finally:
        db.close()

from .inventory import Inventory
from .person import Person
from .product import Product
from .product_count import ProductCount
from .warehouse import Warehouse
