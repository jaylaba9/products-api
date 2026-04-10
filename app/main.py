from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

# Database COLD START
# takes class 'Base' (it knows all models, as Product inherits after Base) and through engine, checks RDS.
# if table 'products' doesn't exist, creates one
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Simple Products API")

@app.get("/")
def root():
  return {"status": "healthy", "architecture": "containers"}

# ==========================================
# 1. GET all products
# ==========================================
# "db: Session = Depends(get_db)" makes magic:
# Before FastAPI calls thif function, it runs 'get_db()', takes the session from it and puts it into 'db'
@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
  # make query to the table linked to model Product and retrieve everything from it: SELECT * FROM products;
  products = db.query(models.Product).all()

  # FastAPI will return data as JSON
  return products

# ==========================================
# 2. CREATE new product
# ==========================================
@app.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
  # translating Pydantic (JSON from the user) to SQLAlchemy (db object) using dictionary unpacking
  new_product = models.Product(**product.model_dump())

  # add new product to current session
  db.add(new_product)

  # commit changes (new ID is created by Postgres)
  db.commit()

  # refresh new_product to retrieve the ID from the db
  db.refresh(new_product)

  return new_product

# ==========================================
# 3. DELETE product by ID 
# ==========================================
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
  # find product, which id is equal to product_id
  product_query = db.query(models.Product).filter(models.Product.id == product_id)

  # get first matching result
  product = product_query.first()

  if product is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with the given ID does not exist")
  
  product_query.delete(synchronize_session=False)

  db.commit()

  return

@app.get("/health")
def health_check():
  # Crucial for ALB
  return {"status": "ok"}

