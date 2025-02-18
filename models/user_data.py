from sqlalchemy import Column, Integer, String
from models.database import Base

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    skin_problems = Column(String, nullable=False)  # Store as comma-separated values
    email = Column(String, unique=True, nullable=False)
