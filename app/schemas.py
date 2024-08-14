from typing import List, Union
from pydantic import BaseModel
import datetime

        
class TokenSchema(BaseModel):
    access_token: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    status:bool
    created_date:datetime.datetime


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserPass(UserBase):
    password: str


class ProductBase(BaseModel):
    id: int
    name: str
    price: int
    quantity:int   #default=1 ??
    measurement_unit:str

    class Config:
        orm_mode = True

# class ProductInBasket(ProductBase):
#     quantity:int   #default=1 ??


class BuyBasketBase(BaseModel):
    id: int
    name: str
    is_active:bool
    user:UserBase

    products: List[ProductBase]
    

    class Config:
        orm_mode = True

class ProductSchema(ProductBase):
    buy_baskets: List[BuyBasketBase]

class User(UserBase):
    id: int
    is_active: bool
    buy_baskets: List[BuyBasketBase] = []

    class Config:
        orm_mode = True 






