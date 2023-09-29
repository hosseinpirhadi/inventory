from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.controller.schema.person import PersonCreate
from src.repository.person_repository import PersonRepository
from src.repository.hash import Hash

class PersonService:
    def __init__(self):
        self.repository = PersonRepository()

    def get_persons(self, db: Session, skip: int, limit: int):
        return self.repository.get_persons(db, skip, limit)

    def get_person_by_id(self, db: Session, person_id: int):
        person = self.repository.get_person_by_id(db, person_id)
        if person:
            return person
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no person with id: {person_id}')

    def create_person(self, db: Session, person: PersonCreate):
        db_person = self.repository.get_person_by_name(db, person.name.strip().lower())
        if db_person:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Person with name: {person.name} already exists')
        return self.repository.create_person(
                                            db,
                                            person.name.strip().lower(),
                                            Hash.bcrypt(person.password)
                                            )

    def delete_person(self, db: Session, person: PersonCreate):
        is_deleted = self.repository.delete_person_by_name(db, person.name.strip().lower())
        if is_deleted:
            return {"message": f"Person {person.name} has been deleted"}
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'There is no person with name {person.name}')