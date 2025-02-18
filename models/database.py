from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./skincare.db"  # Ensure this is correct

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import all models here
from models.product import Product
from models.user_data import UserData  # Import the new model

# Create all tables
Base.metadata.create_all(bind=engine)
