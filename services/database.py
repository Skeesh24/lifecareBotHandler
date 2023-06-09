from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from config import Config


# ====== export ====== #
engine = create_engine(url=Config.MYSQL_CONNECTION_STRING, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
db = SessionLocal()
base = declarative_base()
metadata = MetaData()
# ====== export ====== #

metadata.create_all(bind=engine)
