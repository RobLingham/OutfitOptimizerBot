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
    Today is {current_date}. Please provide a detailed weather forecast for Asheville, NC, including:
    - Temperature at 9 AM
    - High temperature for the day
    - Humidity levels
    - Wind conditions
    - Any chance of precipitation

    Based on this weather information, suggest a detailed outfit for Rob, who will be dropping off his daughter at school and then working from home for the rest of the day. Rob prefers casual, comfortable clothing and may need to adapt to temperature changes. His clothing options include:

    Tops: T-shirts, long sleeve T-shirts, Henleys, short sleeve button-ups, polo shirts, zip sweatshirts, button-ups/flannels, sweatshirts, cardigans, hoodies
    Bottoms: Pants, shorts
    Footwear: Vans shoes, sneakers, Teva sandals, hiking boots
    Outerwear: Puffer jacket, rain jacket, chore jacket
    Socks: Ankle socks, tube socks, wool socks

    Provide a comprehensive outfit suggestion for the day, including:
    - Specific items for each part of the outfit (top, bottom, footwear, outerwear if needed)
    - Reasoning for each choice based on the weather and Rob's activities
    - Suggestions for adapting the outfit if the weather changes throughout the day

    Also, include a philosophical quote from Marcus Aurelius, Pascal, or a similar philosopher for inspiration, along with a brief explanation of how it relates to Rob's day or the weather.

    Format the response as follows:
    Weather: [Detailed weather description]
    Outfit: [Comprehensive outfit suggestion with explanations]
    Quote: [Inspirational quote and its relevance]
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

        return weather, outfit, quote
    except Exception as e:
        logger.error(f"Error parsing outfit suggestion: {str(e)}")
        logger.warning("Using default values due to parsing error")
        return default_weather, default_outfit, default_quote

# Test function
def test_parse_outfit_suggestion():
    test_suggestion = """
    Weather: Partly cloudy with a temperature of 65°F (18°C) at 9 AM, rising to a high of 78°F (26°C) later in the day. Humidity is moderate at 60%. Light breeze with wind speeds of 5-10 mph. There's a 20% chance of light showers in the afternoon.

    Outfit: For Rob's day of dropping off his daughter and working from home, here's a comprehensive outfit suggestion:

    Top: Start with a light blue Henley shirt. The long sleeves will provide warmth in the cooler morning, but can be easily rolled up if it gets warmer. The Henley style offers a casual yet put-together look.

    Bottom: Opt for a pair of comfortable khaki pants. They're versatile enough for the school drop-off and suitable for a work-from-home day. The neutral color pairs well with the light blue top.

    Footwear: Choose the Vans shoes. They're casual and comfortable, perfect for driving and walking during the school drop-off. They also transition well for a day at home.

    Socks: Wear ankle socks with the Vans for a clean, casual look.

    Outerwear: Bring along the chore jacket. It's light enough for the mild temperature but provides an extra layer for the cooler morning or in case of light showers. The jacket can be easily removed once back home.

    Adapting to weather changes:
    - If it gets warmer in the afternoon, Rob can remove the chore jacket and roll up the sleeves of his Henley.
    - In case of light showers, the chore jacket will provide some protection. If Rob needs to step out, he can easily throw it on.
    - If the temperature drops unexpectedly, the long sleeves of the Henley and the chore jacket should provide adequate warmth.

    Quote: "The happiness of your life depends upon the quality of your thoughts." - Marcus Aurelius

    This quote is particularly relevant to Rob's day. As he transitions from the potentially hectic morning routine of dropping off his daughter to a day of working from home, it's a reminder that his mindset and perspective can greatly influence his experience. Just as he's prepared for various weather possibilities with adaptable clothing choices, he can also adapt his thoughts to make the most of his day, regardless of any challenges that may arise.
    """
    weather, outfit, quote = parse_outfit_suggestion(test_suggestion)
    logger.info("Test parse_outfit_suggestion results:")
    logger.info(f"Weather: {weather}")
    logger.info(f"Outfit: {outfit}")
    logger.info(f"Quote: {quote}")

if __name__ == "__main__":
    test_parse_outfit_suggestion()
