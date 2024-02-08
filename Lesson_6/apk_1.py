from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class User(BaseModel):
    username: str = Field(max_length=10)
    full_name: str = None
    age: int = Field(default=0)

class Order(BaseModel):
    items: List[Item]
    user: User