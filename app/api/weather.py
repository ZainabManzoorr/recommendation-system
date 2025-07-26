from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router setup
router = APIRouter()

# --- Pydantic Request Model ---
class LocationInput(BaseModel):
    user_id: str
    latitude: float
    longitude: float

# --- Enum validation helper ---
ALLOWED_WEATHER_ENUMS = {
    "Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm",
    "Snow", "Mist", "Fog", "Haze", "Dust", "Smoke", "Sand"
}

def map_weather_condition(raw_condition: str) -> str:
    """Map and validate OpenWeatherMap conditions to enum-safe values."""
    return raw_condition if raw_condition in ALLOWED_WEATHER_ENUMS else "Clear"

# --- Main Route ---
@router.post("/update-location-weather")
def update_location_and_weather(data: LocationInput):
    try:
        logger.info(f"Incoming request data: {data}")

        # 1. Update user's location
        update_resp = supabase.table("users") \
            .update({
                "latitude": data.latitude,
                "longitude": data.longitude
            }) \
            .eq("id", data.user_id) \
            .execute()

        if not update_resp.data:
            raise HTTPException(status_code=404, detail="User not found")

        logger.info("User location updated successfully.")

        # 2. Get weather from OpenWeatherMap
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={data.latitude}&lon={data.longitude}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        )
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch weather data")

        weather_json = weather_response.json()
        temperature = weather_json["main"]["temp"]
        raw_condition = weather_json["weather"][0]["main"]
        condition = map_weather_condition(raw_condition)

        logger.info(f"Weather fetched: {temperature}°C, {condition}")

        # 3. Insert weather context
        now = datetime.utcnow()
        insert_resp = supabase.table("user_weather_context").insert({
            "id": str(uuid.uuid4()),
            "user_id": data.user_id,
            "temperature": temperature,
            "weather_condition": condition,
            "timestamp": now.isoformat(),
            "date": now.date().isoformat()
        }).execute()

        logger.info("Weather context inserted successfully.")

        return {
            "message": "Location and weather updated successfully.",
            "weather": {
                "temperature": temperature,
                "condition": condition
            }
        }

    except Exception as e:
        logger.exception("Unhandled error in /update-location-weather")
        raise HTTPException(status_code=500, detail=str(e))
