from aiogram.types import LabeledPrice
from services.database import base, metadata
from sqlalchemy import Column, Integer, Table, String, Float, text
from sqlalchemy.orm import Session
from pydantic import BaseModel


subs_table = Table(
    "Subscriptions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("price", Integer, nullable=False),
)


class Subs(base):
    __tablename__: str = "Subscriptions"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)
    price = Column("price", Integer, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.price}'


def getSubFromCallbackData(db: Session, data: str) -> LabeledPrice:
    query = subs_table.select().where(subs_table.c.name == data)

    row = db.execute(query).first()

    res = dict(zip(row._fields, row.t))

    return LabeledPrice(data, res["price"]*100)
