from openai import OpenAI
from config import CLOTHING_OPTIONS, OPENAI_API_KEY
from datetime import datetime
from weather import get_weather

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_outfit_suggestion():
    current_date = datetime.now().strftime("%Y-%m-%d")
    weather_data = get_weather()
    
    prompt = f"""
    Today is {current_date}. The current weather in Asheville, NC is:
    Temperature: {weather_data['temperature']}°F
    Description: {weather_data['description']}
    Humidity: {weather_data['humidity']}%
    Wind Speed: {weather_data['wind_speed']} mph

    Please provide an appropriate outfit suggestion for today, including a top, bottom, footwear, and accessories if necessary.
    Consider the temperature, weather conditions, and comfort.

    Use the following clothing options:
    {CLOTHING_OPTIONS}

    Also, provide a short philosophical quote for inspiration.

    Format the response as follows:
    Weather: [Brief weather description]
    Outfit: [Detailed outfit suggestion]
    Quote: [Inspirational quote]
    """

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return completion.choices[0].message.content

def parse_outfit_suggestion(suggestion):
    lines = suggestion.split('\n')
    weather = next((line.split(': ')[1] for line in lines if line.startswith('Weather:')), '')
    outfit = next((line.split(': ')[1] for line in lines if line.startswith('Outfit:')), '')
    quote = next((line.split(': ')[1] for line in lines if line.startswith('Quote:')), '')
    return weather, outfit, quote
