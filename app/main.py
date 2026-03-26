from fastapi import FastAPI

app = FastAPI(title="Simple Products API")

@app.get("/")
def root():
  return {"status": "healthy", "architecture": "containers"}

@app.get("/products")
def get_products():
  #TO DO: fetching from RDS
  return [{"id": 1, "name": "Notebook", "price": 999}]

@app.get("/health")
def health_check():
  # Crucial for ALB
  return {"status": "ok"}

