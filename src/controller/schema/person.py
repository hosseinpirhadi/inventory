from pydantic import BaseModel

class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    password: str

class Person(PersonBase):
    id: int

    class Config:
        orm_mode = True