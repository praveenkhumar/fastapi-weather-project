# Weather API with FastAPI: A Comprehensive Learning Guide

## 1. Project Overview and Learning Objectives

### Project Goal

Create a robust, production-ready Weather API that demonstrates:

- RESTful API design principles
- External API integration
- Input validation
- Error handling
- API documentation

### Learning Outcomes

By the end of this guide, you'll understand:

- How to build a FastAPI application
- Integrating third-party APIs
- Using Pydantic for data validation
- Implementing error handling
- Generating automatic API documentation

## 2. Project Setup

### Prerequisites

- Python 3.8+
- OpenWeather API Account (Free tier)
- Basic understanding of Python and REST APIs

### Step-by-Step Environment Setup

#### Create a project directory:

```bash
mkdir fastapi-weather-project
cd fastapi-weather-project
```

#### Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### Install required dependencies:

```bash
pip install fastapi uvicorn requests pydantic python-dotenv
```

## 3. Project Structure

```
fastapi-weather-project/
│
├── .env                    # Environment variables
├── main.py                 # Main FastAPI application
├── models.py               # Pydantic models
├── services.py             # External API service
└── requirements.txt        # Project dependencies
```

## 4. Implementing the Weather API

### 4.1 Environment Configuration

Create a `.env` file for API key management:

```ini
OPENWEATHER_API_KEY=your_api_key_here
```

### 4.2 Pydantic Models (`models.py`)

```python
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
```

### 4.3 Weather Service (`services.py`)

```python
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
            response.raise_for_status()

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
```

### 4.4 Main Application (`main.py`)

```python
from fastapi import FastAPI, Depends
from models import WeatherRequest, WeatherResponse
from services import WeatherService

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
```

## 5. Running the Application

#### Generate requirements file:

```bash
pip freeze > requirements.txt
```

#### Run the application:

```bash
uvicorn main:app --reload
```

#### Access API Documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 6. Advanced Learning Challenges

- Implement caching to reduce external API calls
- Add more error handling for city not found scenarios
- Create unit tests for models and services
- Implement rate limiting
- Add support for retrieving weather by coordinates

## 7. Best Practices and Learning Notes

### API Design

- Use Pydantic for strong type validation
- Implement clear, descriptive error messages
- Follow RESTful design principles

### Security Considerations

- Never commit API keys to version control
- Use environment variables
- Implement proper error handling

### Performance Tips

- Use async capabilities of FastAPI
- Implement caching mechanisms
- Minimize external API call overhead

## 8. Deployment Considerations

- Use HTTPS in production
- Implement proper environment management
- Consider containerization with Docker
- Use production ASGI servers like Gunicorn

## Conclusion

This project demonstrates building a robust, scalable Weather API using modern Python frameworks. It combines technical implementation with educational insights, helping you understand API development best practices.
