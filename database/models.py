import uuid
import time
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from database.sql_client import Base

def generate_uuid():
    return str(uuid.uuid4())

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)
    grocery_lists = relationship("GroceryList", cascade='all, delete-orphan')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



grocery_list_item_table = Table('grocery_list_item', Base.metadata,
                                Column('grocery_list_id', ForeignKey('grocery_lists.id')),
                                Column('grocery_item_id', ForeignKey('grocery_items.id')))


class GroceryList(Base):
    __tablename__ = 'grocery_lists'
    id = Column(String, primary_key=True, default=generate_uuid)
    customer_id = Column(String, ForeignKey('customers.id'))
    desired_delivery = Column(Float)
    total_price = Column(Integer)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)
    grocery_items = relationship("GroceryItem", secondary=grocery_list_item_table)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class GroceryItem(Base):
    __tablename__ = 'grocery_items'
    id = Column(String, primary_key=True, default=generate_uuid)
    price_per_unit = Column(Integer)
    quantity = Column(Integer)
    name = Column(String)
    type = Column(String)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
