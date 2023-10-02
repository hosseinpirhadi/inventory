from fastapi import HTTPException, status
from sqlalchemy import and_, update
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

from src.repository.models import ProductCount, Product


class ProductCountRepository:
    def __init__(self):
        pass

    def get_products_by_warehouse_id(self, db: Session, warehouse_id: int, skip: int, limit: int):
        return db.query(ProductCount).filter(ProductCount.ware_house_id == warehouse_id).\
                                            order_by(ProductCount.id).offset(skip).limit(limit).all()

    def get_warehouse_report(self, db: Session, warehouse_id: int, skip: int, limit: int):
        product = aliased(Product)

        query = (
            db.query(ProductCount, product)
            .join(product, ProductCount.id == product.id)
            .filter(ProductCount.ware_house_id == warehouse_id)
        )

        query = query.order_by(product.id).offset(skip).limit(limit)

        results = query.all()

        return results

    def get_product_by_product_id_and_warehouse_id(self, db:Session, product_id: int, warehouse_id: int):
        return db.query(ProductCount).filter(and_(ProductCount.product_id == product_id,
                                                            ProductCount.ware_house_id == warehouse_id)).first()

    def get_warehouses_by_product_id(self, db:Session, product_id: int, skip: int, limit: int):
        return db.query(ProductCount).filter(ProductCount.product_id == product_id).\
            order_by(ProductCount.id).offset(skip).limit(limit).all()

    def add_product_amount(self, db:Session, product_id: int, warehouse_id: int, amount: int):
        product_count = ProductCount(product_id=product_id,
                                    ware_house_id=warehouse_id,
                                    amount=amount)
        db.add(product_count)
        db.commit()
        db.refresh(product_count)
        return product_count

    def _add_product_amount(self, db:Session, product_id: int, warehouse_id: int, amount: int):
        product_count = ProductCount(product_id=product_id,
                                    ware_house_id=warehouse_id,
                                    amount=amount)
        db.add(product_count)
        db.commit()
        db.refresh(product_count)
        return product_count

    def get_product_amount(self, db: Session, product_id: int, ware_house_id: int):
        amount = db.query(ProductCount.amount).filter(
            (ProductCount.product_id == product_id) & (ProductCount.ware_house_id == ware_house_id)
        ).scalar()

        return amount

    def update_product_amount(self, db:Session, product_id: int, warehouse_id: int, additional_amount: int):

        current_amount = self.get_product_amount(db, product_id, warehouse_id)

        if current_amount is None:
            return None

        new_amount = current_amount + additional_amount

        statement = update(ProductCount).where(
                    (ProductCount.product_id == product_id) & (ProductCount.ware_house_id == warehouse_id)
                ).values(amount=new_amount)

        db.execute(statement)
        db.commit()

        return {
            'product_id': product_id,
            'ware_house_id': warehouse_id,
            'amount': new_amount
        }

    def _update_product_amount(self, db:Session, product_id: int, warehouse_id: int, additional_amount: int):

        current_amount = self.get_product_amount(db, product_id, warehouse_id)

        if current_amount is None:
            return None

        new_amount = current_amount + additional_amount

        statement = update(ProductCount).where(
                    (ProductCount.product_id == product_id) & (ProductCount.ware_house_id == warehouse_id)
                ).values(amount=new_amount)

        db.execute(statement)
        db.flush()

        return {
            'product_id': product_id,
            'ware_house_id': warehouse_id,
            'amount': new_amount
        }
