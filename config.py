import os

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Slack API configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN environment variable is not set")

SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
if not SLACK_CHANNEL:
    raise ValueError("SLACK_CHANNEL environment variable is not set")

# City configuration
CITY = "Asheville,US"

# Clothing options
CLOTHING_OPTIONS = {
    "tops": ["T-shirts", "long sleeve T-shirts", "Henleys", "short sleeve button-ups", "polo shirts", "zip sweatshirts", "button-ups/flannels", "sweatshirts", "cardigans", "hoodies"],
    "bottoms": ["pants", "shorts"],
    "footwear": ["Vans shoes", "sneakers", "Teva sandals", "hiking boots"],
    "outerwear": ["puffer jacket", "rain jacket", "chore jacket"],
    "socks": ["ankle socks", "tube socks", "wool socks"]
}
