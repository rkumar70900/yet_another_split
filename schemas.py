from pydantic import BaseModel
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    """
    Base model for user data containing the common fields.
    
    Attributes:
    - name: The name of the user.
    - email: The email address of the user.
    """
    name: str
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits from UserBase.
    """
    pass

class User(UserBase):
    """
    Schema representing a user including additional fields for
    database interaction.

    Attributes:
    - user_id: Unique identifier for the user.
    - created_at: Timestamp of when the user was created.
    """
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    """
    Base model for expense data containing common fields.
    
    Attributes:
    - description: Description of the expense.
    - amount: The amount of the expense.
    - user_id: ID of the user who created the expense.
    """
    description: str
    amount: float
    user_id: int

class ExpenseCreate(ExpenseBase):
    """
    Schema for creating a new expense including additional information
    about which friends are included in the expense.

    Attributes:
    - friends: List of user IDs who are involved in the expense.
    """
    friends: List[int]

class Expense(ExpenseBase):
    """
    Schema representing an expense including additional fields for
    database interaction.

    Attributes:
    - expense_id: Unique identifier for the expense.
    - added_at: Timestamp of when the expense was added.
    """
    expense_id: int
    added_at: datetime

    class Config:
        orm_mode = True

class SplitBase(BaseModel):
    """
    Base model for expense split data containing common fields.
    
    Attributes:
    - expense_id: ID of the expense that is being split.
    - user_id: ID of the user who is part of the split.
    - amount: Amount of money the user owes or is owed.
    """
    expense_id: int
    user_id: int
    amount: float

class Split(SplitBase):
    """
    Schema representing an expense split including additional fields for
    database interaction.

    Attributes:
    - split_id: Unique identifier for the split record.
    """
    split_id: int

    class Config:
        orm_mode = True

class FriendBase(BaseModel):
    """
    Base model for friend relationship data containing common fields.
    
    Attributes:
    - user_id: ID of the user.
    - friend_user_id: ID of the friend of the user.
    """
    user_id: int
    friend_user_id: int

class Friend(FriendBase):
    """
    Schema representing a friendship including additional fields for
    database interaction.

    Attributes:
    - added_at: Timestamp of when the friendship was established.
    """
    added_at: datetime

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    """
    Base model for group data containing the group name.
    
    Attributes:
    - group_name: Name of the group.
    """
    group_name: str

class GroupCreate(GroupBase):
    """
    Schema for creating a new group including the ID of the user
    who is creating the group.

    Attributes:
    - creator_id: ID of the user creating the group.
    """
    creator_id: int

class Group(GroupBase):
    """
    Schema representing a group including additional fields for
    database interaction.

    Attributes:
    - group_id: Unique identifier for the group.
    - created_at: Timestamp of when the group was created.
    - creator: User object representing the creator of the group.
    """
    group_id: int
    created_at: datetime
    creator: User

    class Config:
        orm_mode = True

class GroupMembershipBase(BaseModel):
    """
    Base model for group membership data containing common fields.
    
    Attributes:
    - group_id: ID of the group.
    - user_id: ID of the user who is a member of the group.
    - added_by_id: ID of the user who added the member to the group.
    """
    group_id: int
    user_id: int
    added_by_id: int

class GroupMembershipCreate(GroupMembershipBase):
    """
    Schema for creating a new group membership. Inherits from
    GroupMembershipBase.
    """
    pass

class GroupMembership(GroupMembershipBase):
    """
    Schema representing a group membership including additional fields
    for database interaction.

    Attributes:
    - id: Unique identifier for the membership record.
    - added_at: Timestamp of when the user was added to the group.
    - group: Group object representing the group to which the user belongs.
    - user: User object representing the member of the group.
    - added_by: User object representing the user who added the member.
    """
    id: int
    added_at: datetime
    group: Group
    user: User
    added_by: User

    class Config:
        orm_mode = True

class GroupExpenseBase(BaseModel):
    group_id: int
    description: str
    added_by: int
    amount: float

class GroupExpenseCreate(GroupExpenseBase):
    pass

class GroupExpense(GroupExpenseBase):
    id: int
    added_at: datetime
    added_by: User
    group_id: Group
    expense_id: Expense

    class Config:
        orm_mode = True

