from fastapi import APIRouter, UploadFile, File, HTTPException
import requests
from config import SKIN_ANALYZE_API_KEY, SKIN_ANALYZE_API_URL  # Import from config

router = APIRouter()

@router.post("/analyze-skin")
async def analyze_skin(image: UploadFile = File(...)):
    # Ensure file is an image
    if not image.filename.endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload a JPG or PNG image.")

    # Read image bytes
    image_bytes = await image.read()

    # Send image to Skin Analyze API
    response = requests.post(
        SKIN_ANALYZE_API_URL,
        files={"image": (image.filename, image_bytes, image.content_type)},
        headers={
            "X-RapidAPI-Key": SKIN_ANALYZE_API_KEY,
            "X-RapidAPI-Host": "skin-analyze.p.rapidapi.com"
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Skin analysis failed.")

    # Extract skin type from response
    skin_analysis = response.json()
    skin_type_code = skin_analysis["result"]["skin_type"]["skin_type"]

    # Map API response to readable skin types
    skin_type_map = {
        0: "oily",
        1: "dry",
        2: "normal",
        3: "combination"
    }
    detected_skin_type = skin_type_map.get(skin_type_code, "unknown")

    return {"skin_type": detected_skin_type}

