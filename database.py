import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = (
    "mysql+pymysql://"
    + os.getenv("DB_USER", "root")
    + ":"
    + os.getenv("DB_PASS", "root")
    + "@"
    + os.getenv("DB_HOST", "localhost")
    + "/"
    + os.getenv("DB_NAME", "fast_crud_db")
)
engine = create_engine(DATABASE_URL, pool_size = 10, max_overflow = 30)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
