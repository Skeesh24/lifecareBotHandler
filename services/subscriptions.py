from aiogram.types import LabeledPrice
from services.database import base
from sqlalchemy import Column, Integer, Table, String, Float
from sqlalchemy.orm import Session


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


def getSubFromCallbackData(db: Session, data: str) -> LabeledPrice:
    id: int

    match data:
        case "standart": id = 1
        case "xtra": id = 2
        case "premium": id = 3

    res = db.get(Subs, {"id": id})

    dict_res = {"label": res.__dict__.get("name")}

    dict_res.update({"amount": res.__dict__.get("price")*100})

    return LabeledPrice(**dict_res)
