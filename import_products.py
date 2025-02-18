import pandas as pd
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.product import Product

# ✅ Update CSV filename
csv_file = "Updated_Product_Data.csv"  # <-- Make sure this is correct

# Load the CSV file
df = pd.read_csv(csv_file)

# ✅ Strip spaces from column names
df.columns = df.columns.str.strip()

# Print actual column names to verify they are now clean
print("Cleaned Columns in CSV:", df.columns.tolist())

# Rename columns to match the database model
df.rename(columns={
    "Packshot": "image_url",
    "Marque": "brand",  # <-- Ensure this is correctly mapped
    "Nom du produit": "product_name",
    "Type de produit": "product_type",
    "Actif": "active_ingredient",
    "Prix": "price",
    "Volume (mL) / Quantité": "quantity",
    "Type de peau": "skin_type",
    "Manque d'éclat": "dullness",
    "Rides": "wrinkles",
    "Rougeurs": "redness",
    "Rides des yeux": "eye_wrinkles",
    "Pores apparentes": "visible_pores",
    "Points noirs": "blackheads",
    "Cernes et poches": "dark_circles_puffiness",
    "Manque de fermeté": "lack_of_firmness",
    "Brillance": "shine",
    "Description": "description"
}, inplace=True)

# ✅ Fix fillna() issues
df["price"] = df["price"].fillna(0)  # Default missing prices to 0
df["skin_type"] = df["skin_type"].fillna("Unknown")  # Default missing skin types

# Convert boolean columns
boolean_columns = ["dullness", "wrinkles", "redness", "eye_wrinkles",
                   "visible_pores", "blackheads", "dark_circles_puffiness",
                   "lack_of_firmness", "shine"]

for col in boolean_columns:
    if col in df.columns:
        df[col] = df[col].astype(bool)

# Save to Database
db: Session = SessionLocal()

# Clear old data (optional: only do this if you want to remove existing products)
db.query(Product).delete()
db.commit()

for _, row in df.iterrows():
    product = Product(
        image_url=row["image_url"],
        brand=row["brand"],
        product_name=row["product_name"],
        product_type=row["product_type"],
        active_ingredient=row["active_ingredient"],
        price=row["price"],
        quantity=row["quantity"],
        skin_type=row["skin_type"],
        dullness=row["dullness"],
        wrinkles=row["wrinkles"],
        redness=row["redness"],
        eye_wrinkles=row["eye_wrinkles"],
        visible_pores=row["visible_pores"],
        blackheads=row["blackheads"],
        dark_circles_puffiness=row["dark_circles_puffiness"],
        lack_of_firmness=row["lack_of_firmness"],
        shine=row["shine"],
        description=row["description"]
    )
    db.add(product)

db.commit()
db.close()

print("✅ Products successfully imported from Updated_Product_Data.csv!")
