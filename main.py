from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import diagnosis, recommendations
from routes.user_data import router as user_data_router  # ✅ Correct Import
 # Add `store_user_data` if not included

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "https://skin-diagnosis-frontend.vercel.app"  # Deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include your routes
app.include_router(diagnosis.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(user_data_router, prefix="/api")  # ✅ Correct Import
  # Ensure this is included

@app.get("/")
def home():
    return {"message": "Skin Diagnosis API is running"}

# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI
# from routes import diagnosis, recommendations, user_data  # Import user_data route

# app = FastAPI()

# # Enable CORS so the frontend (React) can communicate with the backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allows requests from React frontend
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# # Include all API routes
# app.include_router(diagnosis.router, prefix="/api")
# app.include_router(recommendations.router, prefix="/api")
# app.include_router(user_data.router, prefix="/api")  # 👈 Add this

# @app.get("/")
# def home():
#     return {"message": "Skin Diagnosis API is running"}
