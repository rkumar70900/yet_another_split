from sqlalchemy.orm import Session
import crud, schema
from exceptions import UserAlreadyExistsException, UserNotFoundException

def create_user_service(db: Session, user: schema.UserCreate):
    existing_user = crud.get_user(db, user_email=user.email)
    if existing_user:
        raise UserAlreadyExistsException()
    return crud.create_user(db, user)

def create_group_service(db: Session, group: schema.GroupCreate):
    existing_user = crud.get_user(db, user_email=group.created_by)
    if not existing_user:
        raise UserNotFoundException()
    return crud.create_group(db, group)

def add_friend_service(db: Session, friend: schema.FriendAdd):
    existing_user  = crud.get_user(db, user_email=friend.user_email)
    if not existing_user:
        raise UserNotFoundException()
    existing_friend = crud.get_user(db, user_email=friend.friend_email)
    if not existing_friend:
        raise UserNotFoundException()
    return crud.add_friend(db, friend)
