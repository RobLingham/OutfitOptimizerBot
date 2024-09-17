import requests
from config import OPENWEATHER_API_KEY, CITY

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")
