from typing import Union, Optional

from pydantic import BaseModel, EmailStr


# создаём модель данных, которая обычно расположена в файле models.py
class User(BaseModel):
    id: int
    name: str


class User1(BaseModel):
    name: str
    age: int
    # is_adult: Union[bool, None] = None


class User2(BaseModel):
    username: str
    message: str


class Feedback(BaseModel):
    username: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_subscribed: bool | None = None


class SearchProducts(BaseModel):
    keyword: str
    category: Union[str, None] = None
    limit: int | None = 10


class User3(BaseModel):
    username: str
    password: str


