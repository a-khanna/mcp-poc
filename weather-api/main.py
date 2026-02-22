from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int


@app.get("/")
def root():
    return {"message": "Weather API"}


@app.get("/weather/{city}", response_model=WeatherResponse)
def get_weather(city: str):
    return WeatherResponse(
        city=city,
        temperature=22.5,
        condition="Sunny",
        humidity=65
    )
