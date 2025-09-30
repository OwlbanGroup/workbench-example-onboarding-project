"""FastAPI backend for the tutorial app."""

import json
import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .database import store_user_data, get_user_data, store_app_data, get_app_data

app = FastAPI(title="Tutorial App Backend", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserData(BaseModel):
    """Model for user data."""

    name: str
    email: str
    progress: Dict[str, Any] = {}


class AppData(BaseModel):
    """Model for application data."""

    key: str
    value: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "tutorial-app-backend"}


logger = logging.getLogger("tutorial_app_backend")
logging.basicConfig(level=logging.DEBUG)


@app.post("/users/{user_id}")
async def create_or_update_user(user_id: str, user_data: UserData):
    """Create or update user data."""
    try:
        # Serialize nested data to JSON string before storing
        user_data_dict = user_data.dict()
        if "progress" in user_data_dict:
            user_data_dict["progress"] = json.dumps(user_data_dict["progress"])
        success = store_user_data(user_id, user_data_dict)
        if not success:
            logger.error("Failed to store user data for user_id=%s", user_id)
            raise HTTPException(status_code=500, detail="Failed to store user data")
        return {"message": "User data stored successfully", "user_id": user_id}
    except Exception as e:
        logger.exception("Exception while storing user data for user_id=%s: %s", user_id, e)
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user data."""
    data = get_user_data(user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "data": data}


@app.post("/data")
async def store_data(app_data: AppData):
    """Store application data."""
    success = store_app_data(app_data.key, app_data.value)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store data")
    return {"message": "Data stored successfully", "key": app_data.key}


@app.get("/data/{key}")
async def get_data(key: str):
    """Get application data."""
    value = get_app_data(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"key": key, "value": value}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
