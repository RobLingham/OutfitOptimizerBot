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
        logger.info("Calling generate_outfit_suggestion function")
        suggestion = generate_outfit_suggestion()
        logger.info("generate_outfit_suggestion function completed")

        logger.info("Calling parse_outfit_suggestion function")
        weather, outfit, quote = parse_outfit_suggestion(suggestion)
        logger.info("parse_outfit_suggestion function completed")
        
        logger.info("Outfit suggestion generated and parsed successfully")
        logger.info(f"Parsed Weather: {weather}")
        logger.info(f"Parsed Outfit: {outfit}")
        logger.info(f"Parsed Quote: {quote}")

        # Check for empty values and use placeholders if necessary
        if not weather.strip():
            weather = "Weather data unavailable"
            logger.warning("Empty weather data, using placeholder")
        if not outfit.strip():
            outfit = "Wear comfortable clothes suitable for working from home"
            logger.warning("Empty outfit suggestion, using placeholder")
        if not quote.strip():
            quote = "The best preparation for tomorrow is doing your best today. - H. Jackson Brown Jr."
            logger.warning("Empty quote, using placeholder")

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
