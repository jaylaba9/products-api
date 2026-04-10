import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try: 
  DB_HOST = os.environ["DB_HOST"]
  DB_NAME = os.environ["DB_NAME"]
  DB_USER = os.environ["DB_USER"]
  DB_PASS = os.environ["DB_PASSWORD"]
except KeyError as e:
  print(f"DB Configuration error: {e}")
  raise

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DB_URL)

# session generator -> each time produces new session linked to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for tables
Base = declarative_base()

def get_db():
  db = SessionLocal()   # open connection
  try:
    yield db
  finally:
    db.close()    # close connection