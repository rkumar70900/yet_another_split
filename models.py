from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User")


class Split(Base):
    __tablename__ = "splits"
    split_id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.expense_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    expense = relationship("Expense")
    user = relationship("User")


class Friend(Base):
    __tablename__ = "friends"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    friend_user_id = Column(Integer, ForeignKey("users.user_id"),
                            primary_key=True)
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_user_id])
