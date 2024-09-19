from openai import OpenAI
from config import CLOTHING_OPTIONS, OPENAI_API_KEY
from datetime import datetime
import logging

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
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        response = completion.choices[0].message.content
        logger.info(f"Generated outfit suggestion: {response}")
        return response
    except Exception as e:
        logger.error(f"Error generating outfit suggestion: {str(e)}")
        raise

def parse_outfit_suggestion(suggestion):
    logger.info(f"Parsing outfit suggestion: {suggestion}")
    lines = suggestion.split('\n')
    weather = next((line.split(': ', 1)[1] for line in lines if line.startswith('Weather:')), '')
    outfit = next((line.split(': ', 1)[1] for line in lines if line.startswith('Outfit:')), '')
    quote = next((line.split(': ', 1)[1] for line in lines if line.startswith('Quote:')), '')
    
    logger.info(f"Parsed weather: {weather}")
    logger.info(f"Parsed outfit: {outfit}")
    logger.info(f"Parsed quote: {quote}")
    
    return weather, outfit, quote
