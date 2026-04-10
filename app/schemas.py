from pydantic import BaseModel

# schema to create product. ID is created by database, so it's missing here
class ProductCreate(BaseModel):
  name: str
  price: float

# schema to return product (api response)
class ProductResponse(ProductCreate):
  id: int

  # instructs pydantic that the data comes from DB objects, and not regular python dicts
  class Config:
    from_attributes = True