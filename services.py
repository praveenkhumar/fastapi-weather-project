import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    @classmethod
    def get_weather(cls, city: str):
        try:
            params = {
                "q": city,
                "appid": cls.API_KEY,
                "units": "metric"  # Use metric for Celsius
            }
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()  # Raise exception for bad responses
            
            data = response.json()
            return {
                "city": data['name'],
                "temperature": data['main']['temp'],
                "feels_like": data['main']['feels_like'],
                "description": data['weather'][0]['description'],
                "humidity": data['main']['humidity'],
                "wind_speed": data['wind']['speed']
            }
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching weather data: {str(e)}"
            )