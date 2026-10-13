import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Credentials lus depuis .env (mêmes variables que mysql_connection.py)
user     = os.getenv("DB_USER",     "root")
password = os.getenv("DB_PASSWORD", "root")
host     = os.getenv("DB_HOST",     "localhost")
port     = int(os.getenv("DB_PORT", "3306"))
database = os.getenv("DB_NAME",     "projet_dev_avance")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
