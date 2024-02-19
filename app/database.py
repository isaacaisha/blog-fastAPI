from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', port=5433, database='fastapi',
#                                user='postgres', password='touremedina',
#                                cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(f'Database connection was succesfull 😎\n')
#         break
#     except Exception as error:
#         print(f'Connecting to database failed:\nError: {error} 😭\n')
#         time.sleep(3)
#         