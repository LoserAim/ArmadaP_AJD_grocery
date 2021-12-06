import uuid
import time
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from database.sql_client import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    username = Column(String, unique=True, required=True)
    password = Column(String, nullable=False, required=True)
    email = Column(String)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)
    grocery_lists = relationship("Grocery_List")
    addresses = relationship("Address")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    customer_id = Column(String, ForeignKey('customers.id'))
    street_name = Column(String)
    city = Column(String)
    state = Column(String)
    type = Column(String)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)


grocery_list_item_table = Table('grocery_list_item', Base.metadata,
                                Column('grocery_list_id', ForeignKey('grocery_lists.id')),
                                Column('grocery_item_id', ForeignKey('grocery_items.id')))


class Grocery_List(Base):
    __tablename__ = 'grocery_lists'
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    customer_id = Column(String, ForeignKey('customers.id'))
    desired_delivery = Column(Float)
    total_price = Column(Integer)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)
    grocery_items = relationship("Grocery_Item", secondary=grocery_list_item_table)


class Grocery_Item(Base):
    __tablename__ = 'grocery_items'
    id = Column(String, primary_key=True, default=str(uuid.uuid4))
    price_per_unit = Column(Integer)
    quantity = Column(Integer)
    name = Column(String, required=True, unique=True)
    type = Column(String)
    created_at = Column(Float, default=round(time.time()))
    updated_at = Column(Float)
