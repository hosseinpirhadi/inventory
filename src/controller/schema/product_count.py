from pydantic import BaseModel

class ProductCountBase(BaseModel):
    product_id: int
    ware_house_id: int

class ProductCountCreate(ProductCountBase):
    amount: int

    class Config:
        orm_mode = True

class ProductCount(ProductCountCreate):
    id: int

    class Config:
        orm_mode = True

class ProductCountReport(ProductCount):
    product_name: str

    class Config:
        orm_mode = True

class ProductCountByWarehouse(BaseModel):
    ware_house_id: int

class ProductCountByProduct(BaseModel):
    product_id: int
