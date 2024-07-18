from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.
    Parameters:
    - db: Session, the database session.
    - user: schemas.UserCreate, the data required to create a new user,
    which includes the name and email.
    Returns:
    - The newly created user object, including the generated user_id and
    creation timestamp.
    """
    # Create an instance of the User model
    db_user = models.User(name=user.name, email=user.email)
    # Add the user to the session and commit it to the database
    db.add(db_user)
    db.commit()
    # Refresh the instance to load the generated user_id and creation timestamp
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """
    Retrieve a user from the database by their user_id.
    Parameters:
    - db: Session, the database session.
    - user_id: int, the ID of the user to retrieve.
    Returns:
    - The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_friends(db: Session, user_id: int):
    """
    Retrieve all friends of a given user.
    Parameters:
    - db: Session, the database session.
    - user_id: int, the ID of the user whose friends are to be retrieved.
    Returns:
    - A list of Friend objects representing the user's friends.
    """
    return db.query(models.Friend).filter(
        models.Friend.user_id == user_id).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    """
    Create a new expense and split it among friends and the creator.
    Parameters:
    - db: Session, the database session.
    - expense: schemas.ExpenseCreate, the data required to create a new
            expense, which includes the description, amount, user_id, and a
            list of friends to split with.
    Returns:
    - The newly created expense object, including the generated expense_id
    and added timestamp.
    Raises:
    - Exception: If not all mentioned friends are friends with the user
                creating the expense.
    """
    # Create an instance of the Expense model
    db_expense = models.Expense(description=expense.description,
                                amount=expense.amount, user_id=expense.user_id)
    # Add the expense to the session and commit it to the database
    db.add(db_expense)
    db.commit()
    # Refresh the instance to load the generated expense_id
    db.refresh(db_expense)
    # Retrieve the list of friends for the user who created the expense
    friends = get_friends(db, expense.user_id)
    friend_ids = [friend.friend_user_id for friend in friends]
    # Include the user who is creating the expense in the list of participants
    all_participants = expense.friends + [expense.user_id]
    # Check if all mentioned friends are friends with the user
    # creating the expense
    if all(friend_id in friend_ids or friend_id == expense.user_id
            for friend_id in expense.friends):
        # Create splits for each participant
        for friend_id in all_participants:
            db_split = models.Split(expense_id=db_expense.expense_id,
                                    user_id=friend_id,
                                    amount=expense.amount/len(all_participants)
                                    )
            db.add(db_split)
        # Commit the splits to the database
        db.commit()
    else:
        # Raise an exception if any mentioned friend is not a friend of the
        # user creating the expense
        raise Exception("All mentioned friends are not friends with "
                        "the user creating the expense")
    return db_expense
