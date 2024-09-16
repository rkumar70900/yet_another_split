from sqlalchemy.orm import Session
import models, schema
from sqlalchemy import and_, distinct, func, case

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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

def create_group(db: Session, group: schema.GroupCreate):
    user = db.query(models.User).filter(models.User.email == group.created_by).first()
    db_group = models.Groups(group_name=group.group_name, created_by=user.user_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

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


