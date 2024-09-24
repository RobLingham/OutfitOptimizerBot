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
    Today is {current_date}. Please provide a detailed weather forecast for today in Asheville, NC, and suggest an outfit for Rob based on the weather and his activities. Use the following JSON format for your response:
    {{
        "weather": {{
            "description": "Detailed weather description for the full day",
            "temperature": {{
                "morning": "Temperature at 9 AM",
                "high": "High temperature for the day",
                "low": "Low temperature for the day"
            }},
            "humidity": "Humidity level",
            "wind": "Wind conditions",
            "precipitation": "Chance of precipitation"
        }},
        "outfit": {{
            "top": "Suggested top",
            "bottom": "Suggested bottom",
            "footwear": "Suggested footwear",
            "outerwear": "Suggested outerwear, if needed",
            "socks": "Suggested socks"
       }},
        "reasoning": "Explanation for outfit choices based on weather and activities",
        "adaptations": "Suggestions for adapting the outfit if weather changes",
        "quote": {{
            "text": "Inspirational quote from a stoic philosopher (e.g., Marcus Aurelius, Seneca) or from philosophers like Pascal or Jung",
            "author": "Quote author",
            "relevance": "Explanation of quote's relevance to the day or weather"
        }}
    }}
    Ensure all outfit suggestions come from Rob's available options:
    {json.dumps(CLOTHING_OPTIONS, indent=4)}
    '''
    try:
        logger.info("Sending request to OpenAI API")
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        response = completion.choices[0].message.content
        logger.info(f"Generated outfit suggestion: {response}")
        return json.loads(response)
    except Exception as e:
        logger.error(f"Error generating outfit suggestion: {str(e)}")
        return None

def format_outfit_suggestion(suggestion):
    if suggestion is None:
        return "Sorry, I couldn't generate an outfit suggestion at this time."

    weather = suggestion['weather']
    outfit = suggestion['outfit']
    quote = suggestion['quote']

    # Capitalize the first letter of each outfit item
    for key in outfit:
        if outfit[key]:
            outfit[key] = outfit[key].capitalize()

    # Process weather description
    weather['description'] = weather['description'].rstrip('.').capitalize()

    template = f"""
Good morning Rob! Here's your outfit suggestion for today in Asheville, NC:

Weather:
{weather['description']}. At 9 AM, the temperature is expected to be around {weather['temperature']['morning']} with a high of {weather['temperature']['high']} and a low of {weather['temperature']['low']}. Humidity levels are {weather['humidity']}, and wind conditions are {weather['wind']}. The chance of precipitation is {weather['precipitation']}.

Outfit:
• Top: {outfit['top']}
• Bottom: {outfit['bottom']}
• Footwear: {outfit['footwear']}
• Outerwear: {outfit.get('outerwear', 'No outerwear needed')}
• Socks: {outfit['socks']}

Reasoning: {suggestion['reasoning']}

Adaptations: {suggestion['adaptations']}

Quote:
"{quote['text']}" — {quote['author']}
{quote['relevance']}
    """
    return template.strip()  # Remove leading/trailing whitespace

if __name__ == "__main__":
    suggestion = generate_outfit_suggestion()
    if suggestion:
        formatted_suggestion = format_outfit_suggestion(suggestion)
        print(formatted_suggestion)
    else:
        print("Failed to generate outfit suggestion")