from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    brand = Column(String, index=True)
    product_name = Column(String, index=True)
    product_type = Column(String)
    active_ingredient = Column(String)
    price = Column(Float)
    quantity = Column(String)
    skin_type = Column(String)

    # Skin concerns (Boolean fields)
    dullness = Column(Boolean, default=False)
    wrinkles = Column(Boolean, default=False)
    redness = Column(Boolean, default=False)
    eye_wrinkles = Column(Boolean, default=False)
    visible_pores = Column(Boolean, default=False)
    blackheads = Column(Boolean, default=False)
    dark_circles_puffiness = Column(Boolean, default=False)
    lack_of_firmness = Column(Boolean, default=False)
    shine = Column(Boolean, default=False)

    description = Column(String)  # <-- ADD THIS LINE
