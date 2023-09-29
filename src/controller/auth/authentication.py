from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.controller.auth.oauth2 import authenticate_user, create_access_token
from src.repository.models import get_db


class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True

router = APIRouter(tags=['authentication'])

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                            db: Session = Depends(get_db)):
    person = authenticate_user(form_data.username, form_data.password, db)
    if not person:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(person.name, person.id, timedelta(minutes=20))

    return Token(access_token=token, token_type="bearer")
