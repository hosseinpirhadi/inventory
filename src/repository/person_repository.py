from sqlalchemy.orm import Session
from src.repository.models import Person
from src.controller.schema.person import PersonCreate
from fastapi import HTTPException

class PersonRepository:
    def __init__(self):
        pass

    def get_persons(self, db: Session, skip: int, limit: int):
        return db.query(Person).order_by(Person.id).offset(skip).limit(limit).all()

    def get_person_by_id(self, db: Session, person_id: int):
        return db.query(Person).filter(Person.id == person_id).first()

    def get_person_by_name(self, db: Session, person_name: str):
        return db.query(Person).filter(Person.name == person_name).first()

    def create_person(self, db: Session, person_name: str, password: str):
        person = Person(name=person_name, password=password)
        db.add(person)
        db.commit()
        db.refresh(person)
        return person

    def delete_person_by_name(self, db: Session, person_name: str):
        person = db.query(Person).filter(Person.name == person_name).first()
        if person:
            db.delete(person)
            db.commit()
            return True
        return False