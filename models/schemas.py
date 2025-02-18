from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    image_url: str
    brand: str
    product_name: str
    product_type: str
    active_ingredient: Optional[str]
    price: float
    quantity: Optional[str]
    skin_type: str

    # Skin concerns
    dullness: bool
    wrinkles: bool
    redness: bool
    eye_wrinkles: bool
    visible_pores: bool
    blackheads: bool
    dark_circles_puffiness: bool
    lack_of_firmness: bool
    shine: bool

    description: Optional[str]

    class Config:
        from_attributes = True  # Required for SQLAlchemy models
