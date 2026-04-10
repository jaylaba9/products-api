from .database import Base
from sqlalchemy import Column, Integer, Float, String

# creating class Product that inherits from Base --> it tells sqlalchemy that this class is a SQL table
class Product(Base):
  __tablename__ = "products"

  # columns:
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  price = Column(Float)