from pydantic import BaseModel, Field, validator
from typing import Optional

class WeatherRequest(BaseModel):
    city: str = Field(..., min_length=2, max_length=50, 
                     description="Name of the city to get weather data")
    
    @validator('city')
    def validate_city_name(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError('City name must contain only alphabetic characters')
        return value.strip()

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float

    class Config:
        schema_extra = {
            "example": {
                "city": "London",
                "temperature": 15.5,
                "feels_like": 14.2,
                "description": "Partly cloudy",
                "humidity": 65,
                "wind_speed": 3.6
            }
        }