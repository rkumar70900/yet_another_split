
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Friends(Base):
    __tablename__ = "friends"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    friend_user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_user_id])

class Groups(Base):
    __tablename__ = "bunch"
    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(255), nullable=False)
    created_by  = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at   = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", foreign_keys=[created_by])

class GroupMembers(Base):
    __tablename__ = "groupmembers"
    groupmember_id = Column(Integer, primary_key=True, index=True)
    groupmember_user_id = Column(Integer, ForeignKey("users.user_id"))
    groupmember_group_id = Column(Integer, ForeignKey("bunch.group_id"))
    added_by  = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    added_at   = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    groupmember = relationship("Groups", foreign_keys=[groupmember_group_id])
    user = relationship("User", foreign_keys=[groupmember_user_id])
    added = relationship("User", foreign_keys=[added_by])

class Expenses(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    group_id = Column(Integer, ForeignKey("bunch.group_id"), nullable=True)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    created_at  = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", foreign_keys=[created_by])
    group = relationship("Groups", foreign_keys=[group_id])

class Splits(Base):
    __tablename__ = "splits"
    split_id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.expense_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at   = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expense = relationship("Expenses", foreign_keys=[expense_id])
    user = relationship("User", foreign_keys=[user_id])

