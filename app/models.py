from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

    buy_baskets = relationship('BuyBasket', back_populates='user')
 

class BasketProduct(Base):
    __tablename__ = 'basket_products'
    product_id = Column(ForeignKey('products.id'), primary_key=True)
    basket_id = Column(ForeignKey('buy_baskets.id'), primary_key=True)
    quantity = Column(Integer, nullable=False,default=1)   #default=1 ??
    product_type = Column(String,nullable=False,default=1) #default=1 ??


class BuyBasket(Base):
    __tablename__ = 'buy_baskets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=False)
    
    user = relationship('User', back_populates='buy_baskets')
    
    # Many-to-many relationship with Product
    products = relationship('Product', secondary="basket_products", back_populates='buy_baskets')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    
    # Many-to-many relationship with BuyBasket
    buy_baskets = relationship('BuyBasket', secondary="basket_products", back_populates='products')


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)

