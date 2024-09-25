from sqlalchemy.orm import Session
import crud
import schema
from exceptions import UserAlreadyExistsException
from exceptions import UserNotFoundException
from exceptions import GroupNotFoundException


def create_user_service(db: Session, user: schema.UserCreate):
    """
    Creates a new user.

    Args:
        db (Session): The database session.
        user (schema.UserCreate): The user to be created.

    Raises:
        UserAlreadyExistsException: If a user with the same email already exists.
        :return: Calls create_user operation in crud module to create the user.

    """
    existing_user = crud.get_user(db, user_email=user.email)
    if existing_user:
        raise UserAlreadyExistsException()
    return crud.create_user(db, user)

def create_group_service(db: Session, group: schema.GroupCreate):
    """Creates a new group.

    Args:
        db (Session): The database session.
        group (schema.GroupCreate): The group to be created.

    Raises:
        UserNotFoundException: If the user who created the group does not exist.
        :return: Calls create_group operation in crud module to create the group.

    """
    existing_user = crud.get_user(db, user_email=group.created_by)
    if not existing_user:
        raise UserNotFoundException()
    return crud.create_group(db, group)

def add_friend_service(db: Session, friend: schema.FriendAdd):
    """Adds a new friendship between two users.

    Args:
        db (Session): The database session.
        friend (schema.FriendAdd): Details of the new friendship to be added.

    Raises:
        UserNotFoundException: If either user does not exist in the system.
        :return: Calls add_friend operation in crud module to create the friendship.

    """
    existing_user  = crud.get_user(db, user_email=friend.user_email)
    if not existing_user:
        raise UserNotFoundException()
    existing_friend = crud.get_user(db, user_email=friend.friend_email)
    if not existing_friend:
        raise UserNotFoundException()
    return crud.add_friend(db, friend)

def add_member_to_group_service(db: Session, group_member: schema.GroupMemberAdd):
    """Adds a member to an existing group.

    Args:
        db (Session): The database session.
        group_member (schema.GroupMemberAdd): Details of the new group member to be added.

    Raises:
        UserNotFoundException: If either user does not exist in the system.
        GroupNotFoundException: If the specified group does not exist.
    :return: Calls add_user_to_group operation in crud module to create the group membership.
    """
    existing_user = crud.get_user(db, user_email=group_member.added_by)
    if not existing_user:
        raise UserNotFoundException()
    existing_group_member = crud.get_user(db, user_email=group_member.groupmember_user_email)
    if not existing_group_member:
        raise UserNotFoundException()
    existing_group = crud.get_group(db, group_member.groupmember_group_id)
    if not existing_group:
        raise GroupNotFoundException()
    return crud.add_user_to_group(db, group_member)


    

