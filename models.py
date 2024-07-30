from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create a base class for declarative models
Base = declarative_base()

class User(Base):
    """
    Represents a user in the system.

    Attributes:
    - __tablename__: Name of the table in the database.
    - user_id: Unique identifier for the user.
    - name: Name of the user.
    - email: Email address of the user (must be unique).
    - created_at: Timestamp of when the user was created.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Expense(Base):
    """
    Represents an expense recorded by a user.

    Attributes:
    - __tablename__: Name of the table in the database.
    - expense_id: Unique identifier for the expense.
    - description: Description of the expense.
    - amount: Amount of the expense.
    - user_id: ID of the user who recorded the expense (foreign key to 'users').
    - added_at: Timestamp of when the expense was added.
    - user: Relationship to the User who recorded the expense.
    """
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User")

class Split(Base):
    """
    Represents a split of an expense among users.

    Attributes:
    - __tablename__: Name of the table in the database.
    - split_id: Unique identifier for the split.
    - expense_id: ID of the related expense (foreign key to 'expenses').
    - user_id: ID of the user who is part of the split (foreign key to 'users').
    - amount: Amount the user owes or is owed from the split.
    - expense: Relationship to the Expense associated with the split.
    - user: Relationship to the User who is part of the split.
    """
    __tablename__ = "splits"

    split_id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.expense_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    expense = relationship("Expense")
    user = relationship("User")

class Friend(Base):
    """
    Represents a friendship between two users.

    Attributes:
    - __tablename__: Name of the table in the database.
    - user_id: ID of the user (primary key, foreign key to 'users').
    - friend_user_id: ID of the user's friend (primary key, foreign key to 'users').
    - added_at: Timestamp of when the friendship was established.
    - user: Relationship to the User who initiated the friendship.
    - friend: Relationship to the User who is the friend.
    """
    __tablename__ = "friends"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    friend_user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_user_id])

class Group(Base):
    """
    Represents a group of users.

    Attributes:
    - __tablename__: Name of the table in the database.
    - group_id: Unique identifier for the group.
    - group_name: Name of the group.
    - created_at: Timestamp of when the group was created.
    - creator_id: ID of the user who created the group (foreign key to 'users').
    - creator: Relationship to the User who created the group.
    """
    __tablename__ = "expense_groups"

    group_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_name = Column(String(255), index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    creator_id = Column(Integer, ForeignKey('users.user_id'))
    creator = relationship("User", foreign_keys=[creator_id])

class GroupMembership(Base):
    """
    Represents a membership of a user in a group.

    Attributes:
    - __tablename__: Name of the table in the database.
    - id: Unique identifier for the membership record.
    - group_id: ID of the group (foreign key to 'expense_groups').
    - user_id: ID of the user who is a member of the group (foreign key to 'users').
    - added_by_id: ID of the user who added the member to the group (foreign key to 'users').
    - added_at: Timestamp of when the user was added to the group.
    - group: Relationship to the Group to which the user belongs.
    - user: Relationship to the User who is a member of the group.
    - added_by: Relationship to the User who added the member to the group.
    """
    __tablename__ = "group_memberships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('expense_groups.group_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    added_by_id = Column(Integer, ForeignKey('users.user_id'))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    group = relationship("Group", foreign_keys=[group_id])
    user = relationship("User", foreign_keys=[user_id])
    added_by = relationship("User", foreign_keys=[added_by_id])
