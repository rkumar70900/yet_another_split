from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create all the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    Parameters:
    - user: UserCreate schema containing the new user's details.
    - db: Database session dependency.
    Returns:
    - The created user with all details including the generated user_id and
    creation timestamp.
    """
    db_user = crud.create_user(db, user)
    return db_user


@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate,
                   db: Session = Depends(get_db)):
    """
    Create a new expense and split it among friends and the creator.
    Parameters:
    - expense: ExpenseCreate schema containing the new expense details,
    including the list of friends to split with.
    - db: Database session dependency.
    Returns:
    - The created expense with all details including the generated expense_id
    and added timestamp.
    Raises:
    - HTTPException: If all mentioned friends are not friends with the
    user creating the expense.
    """
    try:
        db_expense = crud.create_expense(db, expense)
        return db_expense
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new group.
    
    Args:
        group (schemas.GroupCreate): Pydantic schema containing group details.
        db (Session, optional): SQLAlchemy database session (injected).
    
    Returns:
        schemas.Group: The created group instance.
    """
    return crud.create_group(db=db, group=group)

@app.post("/groups/{group_id}/members/", response_model=schemas.GroupMembership)
def add_member_to_group(
    group_id: int, membership: schemas.GroupMembershipCreate, db: Session = Depends(get_db)
):
    """
    Endpoint to add a new member to a group.

    Args:
    - group_id (int): The ID of the group to which the new member is being added.
    - membership (schemas.GroupMembershipCreate): The membership data including user_id and added_by_id.
    - db (Session): The database session.

    Returns:
    - schemas.GroupMembership: The newly created group membership entry.

    Raises:
    - HTTPException: 404 if the group is not found.
    - HTTPException: 403 if the user adding the new member is not the group creator or a member of the group.
    """
    # Check if the group exists
    group = db.query(models.Group).filter(models.Group.group_id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if the user adding the member is the creator of the group or a member of the group
    is_creator = group.creator_id == membership.added_by_id
        
    # Check if the user adding the member is already a member of the group
    is_member = db.query(models.GroupMembership).filter(
        models.GroupMembership.group_id == group_id,
        models.GroupMembership.user_id == membership.added_by_id
    ).first()

    # Only allow the group creator or current members to add new members
    if not is_creator and not is_member:
        raise HTTPException(status_code=403, detail="Only group members or the creator can add new members")
    
    # Call CRUD operation to add the new member to the group
    return crud.add_member_to_group(db=db, membership=membership)
