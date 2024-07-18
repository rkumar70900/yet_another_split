from pydantic import BaseModel
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    description: str
    amount: float
    user_id: int


class ExpenseCreate(ExpenseBase):
    friends: List[int]


class Expense(ExpenseBase):
    expense_id: int
    added_at: datetime

    class Config:
        orm_mode = True


class SplitBase(BaseModel):
    expense_id: int
    user_id: int
    amount: float


class Split(SplitBase):
    split_id: int

    class Config:
        orm_mode = True


class FriendBase(BaseModel):
    user_id: int
    friend_user_id: int


class Friend(FriendBase):
    added_at: datetime

    class Config:
        orm_mode = True
