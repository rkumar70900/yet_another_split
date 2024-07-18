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
