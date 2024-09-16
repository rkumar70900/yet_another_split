from pydantic import BaseModel
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FriendBase(BaseModel):
    user_email: str
    friend_email: str

class FriendAdd(FriendBase):
    pass

class Friend(BaseModel):
    user_id: int
    friend_user_id: int
    added_at: datetime

    class Config:
        orm_mode = True

class GroupCreate(BaseModel):
    group_name: str
    created_by: str

class Group(BaseModel):
    group_id: int
    group_name: str
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class GroupMemberBase(BaseModel):
    groupmember_user_email: str
    groupmember_group_id: int

class GroupMemberAdd(GroupMemberBase):
    added_by: str

class GroupMember(GroupMemberBase):
    groupmember_id: int
    added_by: int
    added_at: datetime
    
    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    description: str
    amount: float

class ExpenseCreate(ExpenseBase):
    group_id: str | None
    created_by: str
    users: List[str]

class Expense(ExpenseBase):
    group_id: int | None
    expense_id: int
    created_by: int
    created_at: datetime


    class Config:
        orm_mode = True

class SplitBase(BaseModel):
    expense_id: int
    user_id: int
    amount: float

class SplitCreate(SplitBase):
    pass

class Split(SplitBase):
    split_id: int
    created_at: datetime

    class Config:
        orm_mode = True