from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Item(Base):
    __tablename__ = "items"

    item_name = Column(String)
    item_id = Column(Integer, primary_key=True, autoincrement=True)

    item_category_id = Column(Integer, nullable=False)

class Category(Base):
    __tablename__ = "categories"

    item_category_id = Column(Integer, primary_key=True,autoincrement=True)
    item_category_name = Column(String)

