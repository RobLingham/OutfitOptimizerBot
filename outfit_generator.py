from openai import OpenAI
from config import CLOTHING_OPTIONS, OPENAI_API_KEY
from datetime import datetime
import logging
import json
import re

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
        return None

def parse_outfit_suggestion(suggestion):
    logger.info(f"Parsing outfit suggestion: {suggestion}")
    default_weather = "Unable to fetch weather data"
    default_outfit = "Wear comfortable clothes suitable for working from home"
    default_quote = "The best preparation for tomorrow is doing your best today. - H. Jackson Brown Jr."

    if suggestion is None:
        logger.error("Received None as suggestion, using default values")
        return default_weather, default_outfit, default_quote

    try:
        logger.info("Attempting to parse suggestion using regex")
        weather_match = re.search(r'Weather:\s*(.*?)(?:\n|$)', suggestion, re.DOTALL)
        outfit_match = re.search(r'Outfit:\s*(.*?)(?:\n(?:Quote:|$)|$)', suggestion, re.DOTALL)
        quote_match = re.search(r'Quote:\s*(.*?)(?:\n|$)', suggestion, re.DOTALL)

        weather = weather_match.group(1).strip() if weather_match else default_weather
        outfit = outfit_match.group(1).strip() if outfit_match else default_outfit
        quote = quote_match.group(1).strip() if quote_match else default_quote

        logger.info(f"Regex parsing results:")
        logger.info(f"Weather: {weather}")
        logger.info(f"Outfit: {outfit}")
        logger.info(f"Quote: {quote}")

        if weather == default_weather or outfit == default_outfit or quote == default_quote:
            logger.warning("One or more fields are using default values after regex parsing")
            logger.info("Attempting fallback parsing method")
            
            lines = suggestion.split('\n')
            weather = next((line.split(': ', 1)[1] for line in lines if line.lower().startswith('weather:')), weather)
            outfit = next((line.split(': ', 1)[1] for line in lines if line.lower().startswith('outfit:')), outfit)
            quote = next((line.split(': ', 1)[1] for line in lines if line.lower().startswith('quote:')), quote)

            logger.info(f"Fallback parsing results:")
            logger.info(f"Weather: {weather}")
            logger.info(f"Outfit: {outfit}")
            logger.info(f"Quote: {quote}")

        return weather, outfit, quote
    except Exception as e:
        logger.error(f"Error parsing outfit suggestion: {str(e)}")
        logger.warning("Using default values due to parsing error")
        return default_weather, default_outfit, default_quote

# Test function
def test_parse_outfit_suggestion():
    test_suggestion = """
    Weather: Sunny with a high of 75°F (24°C) and a low of 60°F (16°C). Mild morning around 65°F (18°C) at 9 AM.
    Outfit: Start with a light blue Henley shirt, paired with comfortable khaki pants. Bring a zip sweatshirt for cooler morning temperatures. Wear Vans shoes for a casual look, and choose ankle socks for comfort.
    Quote: "The happiness of your life depends upon the quality of your thoughts." - Marcus Aurelius
    """
    weather, outfit, quote = parse_outfit_suggestion(test_suggestion)
    logger.info("Test parse_outfit_suggestion results:")
    logger.info(f"Weather: {weather}")
    logger.info(f"Outfit: {outfit}")
    logger.info(f"Quote: {quote}")

if __name__ == "__main__":
    test_parse_outfit_suggestion()
