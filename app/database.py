import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8mb4".format(
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD.get_secret_value(),
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        name=settings.DB_NAME,

    ),
    connect_args={"ssl": {"ca": "/app/ca.pem"}} if os.getenv("APP_ENV") == "production" else {},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()