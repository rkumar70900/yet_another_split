from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
import models
import schema
from sqlalchemy import and_
from sqlalchemy import distinct
from sqlalchemy import func

"""
Creates a new user in the database.

 Args:
    db (Session): The SQLAlchemy session.
    user (schema.UserCreate): The user to create, containing their first name, last name, and email.

 Returns:
    models.User: The newly created user object.

 Notes:
    This function adds the new user to the database using the provided SQLAlchemy session,
    then commits the changes. It also refreshes the new user object to ensure it has the
    latest data from the database.
"""
def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""
Adds a new friend to the database if they don't already exist as friends.

 Args:
    db (Session): The SQLAlchemy session.
    friend (schema.FriendAdd): A dictionary containing the email addresses of two users.

 Returns:
    models.Friends: The newly created friendship object, or None if the users are already friends.

 Notes:
    This function first checks if both users exist in the database. If they do not,
    it raises an exception. Then, it queries the database to see if the two users
    are already friends. If they are not, it creates a new friendship object and adds
    it to the database.
"""
def add_friend(db: Session, friend: schema.FriendAdd):
    user_id = db.query(models.User).filter(models.User.email == friend.user_email).first()
    friend_id = db.query(models.User).filter(models.User.email == friend.friend_email).first()
    results = db.query(models.Friends).filter(and_(models.Friends.user_id == user_id.user_id, models.Friends.friend_user_id == friend_id.user_id)).all()
    if not results:
        db_friend = models.Friends(user_id=user_id.user_id, friend_user_id=friend_id.user_id)
        db.add(db_friend)
        db.commit()
        db.refresh(db_friend)
        return db_friend
    else:
        raise Exception({"error": f"{user_id.first_name} and {friend_id.first_name} are already friends"})

"""
Creates a new group in the database.

 Args:
    db (Session): The SQLAlchemy session.
    group (schema.GroupCreate): A dictionary containing information about the new group, including its name
                                 and the email of the user who created it.

 Returns:
    models.Groups: The newly created group object.

 Notes:
    This function first checks if the user exists in the database. If they do not,
    it raises an exception. Then, it creates a new group object and adds it to the database.
    It also adds the creator of the group as its member.
"""
def create_group(db: Session, group: schema.GroupCreate):
    try:
        user = db.query(models.User).filter(models.User.email == group.created_by).first()
        if not user:
            raise Exception({"error": f"User {group.created_by} does not exist"})
        db_group = models.Groups(group_name=group.group_name, created_by=user.user_id)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        user_to_group = {
                        "groupmember_user_email": group.created_by, 
                        "groupmember_group_id": db_group.group_id, 
                        "added_by": user.user_id
        }
        db_group_member = add_user_to_group(db, user_to_group)
        print(db_group_member)
        return db_group
    except Exception as e:
        db.rollback()
        raise e

def add_user_to_group(db: Session, group_member: schema.GroupMemberAdd):
    user = db.query(models.User).filter(models.User.email == group_member.groupmember_user_email).first()
    group = db.query(models.Groups).filter(models.Groups.group_id == group_member.groupmember_group_id).first()
    added_by = db.query(models.User).filter(models.User.email == group_member.added_by).first()
    results = db.query(models.GroupMembers).filter(and_(models.GroupMembers.groupmember_group_id == group.group_id, models.GroupMembers.groupmember_user_id == user.user_id)).all()
    if not results:
        db_groupMember = models.GroupMembers(groupmember_group_id=group.group_id, groupmember_user_id=user.user_id, added_by=added_by.user_id)
        db.add(db_groupMember)
        db.commit()
        db.refresh(db_groupMember)
        return db_groupMember
    else:
        raise Exception({"error": f"{group_member.groupmember_user_email} is already in {group.group_name}"})

def add_expense(db: Session, expense: schema.ExpenseCreate):
    user = db.query(models.User).filter(models.User.email == expense.created_by).first()
    if expense.group_id != '':
        group = db.query(models.Groups).filter(models.Groups.group_id == int(expense.group_id)).first()
        db_expense = models.Expenses(amount=expense.amount, description=expense.description, created_by=user.user_id, group_id=int(group.group_id))
    else:
        db_expense = models.Expenses(amount=expense.amount, description=expense.description, created_by=user.user_id)    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    all_users = expense.users + [expense.created_by]
    each_split = expense.amount/len(all_users)
    for each_user in all_users:
        user  = db.query(models.User).filter(models.User.email == each_user).first()
        db_expenseSplit = models.Splits(expense_id=db_expense.expense_id, user_id=user.user_id, amount=each_split)
        db.add(db_expenseSplit)
        db.commit()
        db.refresh(db_expenseSplit)
    return db_expense

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_all_expenses(db: Session, user_email):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    return db.query(models.Expenses).filter(models.Expenses.created_by == user.user_id)

def total_owed_by_the_user(db: Session, user_email):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    subquery = db.query(distinct(models.Expenses.expense_id)).filter(models.Expenses.created_by == user.user_id)

    # total amount the user owes to all other users
    owed = db.query(func.sum(models.Splits.amount)).filter(
        models.Splits.user_id == user.user_id,
        models.Splits.expense_id.notin_(subquery)
    ).scalar()

    # total amount other users owes to the user
    owes = db.query(func.sum(models.Splits.amount)).filter(
        models.Splits.expense_id.in_(subquery),
        models.Splits.user_id != user.user_id
    ).scalar()

    total = owed - owes

    if total < 0:
        return {'result': f"You are owed {str(-1 * total)}"}
    else:
        return {'result': f"You owe {str(total)}" }
    
def get_user(db: Session, user_email):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    return user

def get_user_by_id(db: Session, user_id):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user

def owed_to_each_user(db: Session, user_email):
    user = get_user(db, user_email)
    a = aliased(models.Expenses)
    b = aliased(models.Splits)
    results = db.query(
        a.created_by, 
        func.sum(b.amount).label('total_amount') 
    ).join(
        b, a.expense_id == b.expense_id 
    ).filter(
        a.created_by != user.user_id, 
        b.user_id == user.user_id 
    ).group_by(
        a.created_by  
    ).all() 
    final = {}
    for row in results:
        final[get_user_by_id(db,row[0]).first_name] = row[1]
    return final

def owed_in_each_group(db: Session, user_email):
    user = get_user(db, user_email)
    Group = aliased(models.Groups)
    Expense = aliased(models.Expenses)
    Split = aliased(models.Splits)

    results = db.query(
        Group.group_name, 
        func.sum(Split.amount).label('total_amount')
    ).join(
        Expense, Expense.group_id == Group.group_id
    ).join(
        Split, Split.expense_id == Expense.expense_id
    ).filter(
        Expense.group_id.isnot(None),
        Split.user_id == user.user_id
    ).group_by(
        Group.group_name
    ).distinct().all()

    final = {}
    for row in results:
        final[row[0]] = row[1] 
    return final

def user_all_groups(db: Session, user_email):
    user = get_user(db, user_email)
    Group = aliased(models.Groups)
    GroupMembers = aliased(models.GroupMembers)

    # Query
    results = db.query(
        Group.group_name
    ).join(
        GroupMembers, GroupMembers.groupmember_group_id == Group.group_id
    ).filter(
        GroupMembers.groupmember_user_id == user.user_id
    ).distinct().all()

    final = [i[0] for i in results]

    return final  


