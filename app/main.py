from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import models
import schema
import services
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schema.User) # what is response model?
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)): # what is depends?
    db_user = services.create_user_service(db, user)
    return db_user

@app.post("/addfriend/", response_model=schema.Friend)
def add_friend(friend: schema.FriendAdd, db: Session = Depends(get_db)):
    db_friend = services.add_friend_service(db, friend)
    return db_friend

@app.post("/groups/", response_model=schema.Group)
def create_group(group: schema.GroupCreate, db: Session = Depends(get_db)):
    db_group = services.create_group_service(db, group)
    return db_group

@app.post("/addmembertogroup/", response_model=schema.GroupMember)
def add_user_to_group(group_member: schema.GroupMemberAdd, db: Session = Depends(get_db)):
    db_groupmeber = services.add_member_to_group_service(db, group_member)
    return db_groupmeber

@app.post("/addexpense", response_model=schema.Expense)
def add_expense(expense: schema.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = crud.add_expense(db, expense)
    return db_expense

@app.get("/users/", response_model=List[schema.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.get("/user_expenses/", response_model=List[schema.Expense])
def get_user_expenses(user_email: str, db: Session = Depends(get_db)):
    return crud.get_all_expenses(db, user_email)

@app.get("/amount_owed/")
def get_amount_owed(user_email: str, db: Session = Depends(get_db)):
    return crud.total_owed_by_the_user(db, user_email)

@app.get("/amount_owed_to_each_user/")
def get_amount_owed_to_each_user(user_email: str, db: Session = Depends(get_db)):
    return crud.owed_to_each_user(db, user_email)

@app.get("/amount_owed_in_each_group/")
def get_amount_owed_to_each_group(user_email: str, db: Session = Depends(get_db)):
    return crud.owed_in_each_group(db, user_email)

@app.get("/all_user_groups")
def get_user_all_groups(user_email: str, db: Session = Depends(get_db)):
    return crud.user_all_groups(db, user_email)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)