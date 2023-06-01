from aiogram.types import LabeledPrice
from services.database import base
from sqlalchemy import Column, Integer, Table, String, Float, text
from sqlalchemy.orm import Session
from pydantic import BaseModel


# subs_table = Table(
#     "Subscriptions",
#     base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(50), nullable=False),
#     Column("price", Float, nullable=False),
# )


class Subs(base):
    __tablename__: str = "Subscriptions"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)
    price = Column("price", Float, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.price}'


class sub(BaseModel):
    id: int
    name: str
    price: int


def getSubFromCallbackData(db: Session, data: str) -> LabeledPrice:
    row = db.execute(
        text(f'SELECT * FROM LIFE_BOT.Subscriptions WHERE name = "{data}"')).first()

    res = dict(zip(row._fields, row.t))

    return LabeledPrice(data, res["price"]*100)
