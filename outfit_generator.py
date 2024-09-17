from openai import OpenAI
from config import CLOTHING_OPTIONS, OPENAI_API_KEY
from datetime import datetime

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_outfit_suggestion():
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
    Today is {current_date}. Consider the current weather in Asheville, NC when suggesting an outfit.
    Please provide an appropriate outfit suggestion for today, including a top, bottom, footwear, and an accessory if necessary.
    Also, provide a short philosophical quote for inspiration.

    Use the following clothing options:
    {CLOTHING_OPTIONS}

    Format the response as follows:
    Weather: [Brief weather description]
    Outfit: [Outfit suggestion]
    Quote: [Inspirational quote]
    """

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return completion.choices[0].message.content

def parse_outfit_suggestion(suggestion):
    lines = suggestion.split('\n')
    weather = next((line.split(': ')[1] for line in lines if line.startswith('Weather:')), '')
    outfit = next((line.split(': ')[1] for line in lines if line.startswith('Outfit:')), '')
    quote = next((line.split(': ')[1] for line in lines if line.startswith('Quote:')), '')
    return weather, outfit, quote