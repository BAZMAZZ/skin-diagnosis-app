import random
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.database import SessionLocal
from models.product import Product
from models.schemas import ProductSchema
from typing import List, Optional

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1️⃣ Get All Products
@router.get("/products", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# 2️⃣ Get a Single Product by ID
@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 3️⃣ Get One Product Per Category for a Given Skin Type (With Fallback)
@router.get("/recommendations", response_model=List[ProductSchema])
def get_recommendations(
    skin_type: Optional[str] = Query(None, description="User's skin type"),
    db: Session = Depends(get_db)
):
    if not skin_type:
        raise HTTPException(status_code=400, detail="Skin type is required")

    query = db.query(Product)

    # Convert French skin types (Database) to English (API Input)
    skin_type_map = {
        "Sensible": "sensitive",
        "Grasse": "oily",
        "Sèche": "dry",
        "Mixte": "combination",
        "Unknown": "unknown"
    }

    reversed_skin_type_map = {v: k for k, v in skin_type_map.items()}  # Reverse mapping
    normalized_skin_type = reversed_skin_type_map.get(skin_type.lower(), skin_type)

    # 🔍 Debug: Check if skin type exists
    print(f"Filtering for skin type: {normalized_skin_type}")

    # Filter products by skin type
    products = query.filter((Product.skin_type == normalized_skin_type) | (Product.skin_type == "Unknown")).all()

    # 🔍 Debug: Check number of filtered products
    print(f"Total matching products for {normalized_skin_type}: {len(products)}")

    # Define product categories with multiple possible names for flexibility
    category_map = {
        "Cleanser": ["cleanser", "face wash", "gel nettoyant", "mousse nettoyante", "nettoyant"],
        "Toner": ["toner", "lotion", "eau tonique"],
        "Serum": ["serum", "ampoule", "essence"],
        "Moisturizer": ["moisturizer", "cream", "gel crème", "lotion hydratante", "hydratant"],
        "Sunscreen": ["sunscreen", "spf", "protection solaire", "sun cream"],
        "Mask": ["mask", "masque", "overnight mask"]
    }

    recommendations = {}

    # Select one random product per category, with fallback logic
    for category, keywords in category_map.items():
        category_products = [
            p for p in products if any(kw in p.product_type.lower() for kw in keywords)
        ]

        if category_products:
            selected_product = random.choice(category_products)
            print(f"Selected {selected_product.product_name} for {category}")  # Debugging
            recommendations[category] = selected_product
        else:
            # 🚨 Fallback: Pick any product from the database for this category
            fallback_products = db.query(Product).filter(
                or_(*[Product.product_type.ilike(f"%{kw}%") for kw in keywords])
            ).all()

            if fallback_products:
                fallback_product = random.choice(fallback_products)
                print(f"Fallback Selected {fallback_product.product_name} for {category}")  # Debugging
                recommendations[category] = fallback_product

    # Convert dictionary to list for API response
    recommended_products = list(recommendations.values())

    # 🔍 Debug: Check final recommendations
    print(f"Total recommended products: {len(recommended_products)}")

    if not recommended_products:
        raise HTTPException(status_code=404, detail="No suitable products found.")




    return recommended_products
