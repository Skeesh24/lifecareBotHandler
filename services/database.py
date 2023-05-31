from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine

from config import Config


# ====== export ====== #
engine = create_engine(
    url=Config.MYSQL_CONNECTION_STRING, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
db = SessionLocal()
base = declarative_base()
# ====== export ====== #

# base.metadata.create_all(bind=engine)

connect = engine.connect()
connect.exec_driver_sql('SELECT * FROM Subscriptions')
