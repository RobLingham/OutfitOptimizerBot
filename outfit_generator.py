from openai import OpenAI
from config import CLOTHING_OPTIONS, OPENAI_API_KEY
from datetime import datetime
import logging
import json

client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

def generate_outfit_suggestion():
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f'''
    Today is {current_date}. Please provide the current weather forecast for Asheville, NC, including the temperature at 9 AM and the high temperature for the day.

    Based on this weather information, suggest an outfit for Rob, who will be dropping off his daughter at school and then working from home for the rest of the day. Rob prefers casual, comfortable clothing and may need to adapt to temperature changes. His clothing options include:

    Tops: T-shirts, long sleeve T-shirts, Henleys, short sleeve button-ups, polo shirts, zip sweatshirts, button-ups/flannels, sweatshirts, cardigans, hoodies
    Bottoms: Pants, shorts
    Footwear: Vans shoes, sneakers, Teva sandals, hiking boots
    Outerwear: Puffer jacket, rain jacket, chore jacket
    Socks: Ankle socks, tube socks, wool socks

    Provide a concise and specific outfit suggestion for the day, avoiding too many options. Also, include a philosophical quote from Marcus Aurelius, Pascal, or a similar philosopher for inspiration.

    Format the response as follows:
    Weather: [Brief weather description]
    Outfit: [Detailed outfit suggestion]
    Quote: [Inspirational quote]
    '''

    try:
        logger.info("Sending request to OpenAI API")
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        response = completion.choices[0].message.content
        logger.info(f"Full OpenAI API response: {json.dumps(completion.model_dump(), indent=2)}")
        logger.info(f"Generated outfit suggestion: {response}")
        return response
    except Exception as e:
        logger.error(f"Error generating outfit suggestion: {str(e)}")
        raise

def parse_outfit_suggestion(suggestion):
    logger.info(f"Parsing outfit suggestion: {suggestion}")
    default_weather = "Unable to fetch weather data"
    default_outfit = "Wear comfortable clothes suitable for working from home"
    default_quote = "The best preparation for tomorrow is doing your best today. - H. Jackson Brown Jr."

    try:
        lines = suggestion.split('\n')
        weather = next((line.split(': ', 1)[1] for line in lines if line.startswith('Weather:')), default_weather)
        outfit = next((line.split(': ', 1)[1] for line in lines if line.startswith('Outfit:')), default_outfit)
        quote = next((line.split(': ', 1)[1] for line in lines if line.startswith('Quote:')), default_quote)
        
        if weather == default_weather or outfit == default_outfit or quote == default_quote:
            logger.warning("One or more fields are using default values")
        
        logger.info(f"Parsed weather: {weather}")
        logger.info(f"Parsed outfit: {outfit}")
        logger.info(f"Parsed quote: {quote}")
        
        return weather, outfit, quote
    except Exception as e:
        logger.error(f"Error parsing outfit suggestion: {str(e)}")
        logger.warning("Using default values due to parsing error")
        return default_weather, default_outfit, default_quote
