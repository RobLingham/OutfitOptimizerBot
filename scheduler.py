from outfit_generator import generate_outfit_suggestion, parse_outfit_suggestion
from slack_bot import send_slack_message
from jinja2 import Template
import os
import time
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def schedule_daily_outfit_suggestion():
    try:
        logger.info("Starting daily outfit suggestion process")

        # Generate outfit suggestion
        suggestion = generate_outfit_suggestion()
        weather, outfit, quote = parse_outfit_suggestion(suggestion)
        
        logger.info("Outfit suggestion generated successfully")
        logger.info(f"Weather: {weather}")
        logger.info(f"Outfit: {outfit}")
        logger.info(f"Quote: {quote}")

        # Prepare message using template
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'outfit_message.txt')
        with open(template_path, 'r') as file:
            template = Template(file.read())

        message = template.render(
            weather=weather,
            outfit=outfit,
            quote=quote
        )
        
        logger.info("Message template rendered")
        logger.info(f"Full rendered message:\n{message}")

        # Add a delay before sending the message
        time.sleep(1)

        # Send message to Slack
        logger.info("Attempting to send message to Slack")
        if send_slack_message(message):
            logger.info("Daily outfit suggestion sent successfully.")
        else:
            logger.error("Failed to send daily outfit suggestion.")

    except Exception as e:
        error_message = f"Error in daily outfit suggestion: {str(e)}"
        logger.error(error_message)
        send_slack_message(error_message)

# For testing purposes
if __name__ == "__main__":
    schedule_daily_outfit_suggestion()
