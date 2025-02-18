from models.database import engine, Base
from models.product import Product  # Ensure Product is imported
from sqlalchemy import inspect

# Use the correct method to check tables in SQLAlchemy 2.0
inspector = inspect(engine)

# Print existing tables before creation
print("Tables before creation:", inspector.get_table_names())

# Force database schema creation
Base.metadata.create_all(bind=engine)

# Print tables after creation
print("Tables after creation:", inspector.get_table_names())

print("✅ Database tables have been successfully created!")
