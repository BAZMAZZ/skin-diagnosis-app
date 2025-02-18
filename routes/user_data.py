from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.user_data import UserData
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schema for validation
class UserDataSchema(BaseModel):
    age: int
    skin_problems: List[str]
    email: str

# Route to store user data
@router.post("/store-user-data")
def store_user_data(user_data: UserDataSchema, db: Session = Depends(get_db)):
    new_user_data = UserData(
        age=user_data.age,
        skin_problems=",".join(user_data.skin_problems),  # Store as comma-separated string
        email=user_data.email
    )
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    return {"message": "User data stored successfully"}
