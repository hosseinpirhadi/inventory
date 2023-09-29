from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Union
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime

class InventoryDateRange(BaseModel):
    start_datetime: Union[str, None] = None
    end_datetime: Union[str, None] = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'InventoryDateRange':
        start_datetime = self.start_datetime
        end_datetime = self.end_datetime
        if start_datetime is None and end_datetime is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='At least one of start_datetime or end_datetime must be provided')
        return self

class InventoryCreate(BaseModel):
    product_id: int
    ware_house_id: int
    delivery_person_id: int
    receiver_person_id: int
    quantity: int
    kind: bool
    created_at: Union[str, None] = None

    class Config:
        orm_mode = True

class ReturnInventory(BaseModel):
    product_id: int
    ware_house_id: int
    delivery_person_id: int
    receiver_person_id: int
    quantity: int
    kind: bool
    created_at: Union[datetime, None] = None

    class Config:
        orm_mode = True

class Inventory(ReturnInventory):
    id: int

    class Config:
        orm_mode = True

class InventoryReport(BaseModel):
    id: int
    product_id: int
    ware_house_id: int
    delivery_person_id: int
    receiver_person_id: int
    kind: bool
    quantity: int
    created_at: str
    receiver_name: str
    delivery_person_name: str

    class Config:
        orm_mode = True