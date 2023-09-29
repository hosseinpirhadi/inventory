from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.controller.schema.person import Person as PersonSchema, PersonBase
from src.controller.schema.person import PersonCreate
from src.repository.models import get_db
from src.services.person_service import PersonService
from src.controller.auth.oauth2 import oauth2_scheme

router = APIRouter(tags=['person'])

person_service = PersonService()

@router.get('/person', response_model=list[PersonSchema], status_code=status.HTTP_200_OK)
def get_persons(skip=0, limit=100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return person_service.get_persons(db, skip, limit)

@router.get('/person/{person_id}', response_model=PersonSchema, status_code=status.HTTP_200_OK)
def get_person(person_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return person_service.get_person_by_id(db, person_id)

@router.post('/person', response_model=PersonSchema, status_code=status.HTTP_201_CREATED)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    return person_service.create_person(db, person)

@router.delete('/person', status_code=status.HTTP_200_OK)
def delete_person(person: PersonBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return person_service.delete_person(db, person)