from fastapi import FastAPI, Depends
from models import WeatherRequest, WeatherResponse
from services import WeatherService
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI(
    title="Weather API",
    description="Get real-time weather information for cities",
    version="1.0.0"
)

@app.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    """
    Fetch weather data for a given city
    
    - **city**: Name of the city (alphabetic characters only)
    - Returns detailed weather information
    """
    weather_data = WeatherService.get_weather(request.city)
    return WeatherResponse(**weather_data)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Weather API"}