from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL
import os
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the values of SLACK_CHANNEL and SLACK_BOT_TOKEN (partially masked)
logger.info(f"SLACK_CHANNEL: {SLACK_CHANNEL}")
logger.info(f"SLACK_BOT_TOKEN: {SLACK_BOT_TOKEN[:10]}...{SLACK_BOT_TOKEN[-5:] if SLACK_BOT_TOKEN else ''}")

client = WebClient(token=SLACK_BOT_TOKEN)

def join_channel():
    try:
        response = client.conversations_join(channel=SLACK_CHANNEL)
        logger.info(f"Bot successfully joined channel {SLACK_CHANNEL}")
        return True
    except SlackApiError as e:
        logger.error(f"Error joining channel: {e}")
        return False

def send_slack_message(message):
    try:
        logger.info(f"Attempting to send message to channel: {SLACK_CHANNEL}")
        
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        logger.info(f"Message sent successfully to channel {SLACK_CHANNEL}")
        logger.info(f"Response: {json.dumps(response.data, indent=2)}")
        return True
    except SlackApiError as e:
        logger.error(f"Error sending message: {e}")
        error_details = e.response['error']
        logger.error(f"Error details: {error_details}")
        logger.error(f"Full error response: {json.dumps(e.response.data, indent=2)}")
        
        if error_details == 'not_in_channel':
            logger.info(f"Bot is not in the channel. Attempting to join...")
            if join_channel():
                logger.info("Successfully joined channel. Retrying message send.")
                return send_slack_message(message)  # Retry sending the message
            else:
                logger.error(f"Failed to join channel {SLACK_CHANNEL}. Please add the bot manually.")
                logger.info("Try using the following command in Slack: /invite @Daily Outfit Suggester")
        elif error_details == 'channel_not_found':
            logger.error(f"The channel {SLACK_CHANNEL} was not found. Please check if the channel ID is correct.")
        elif error_details == 'invalid_auth':
            logger.error("Invalid authentication. Please check the SLACK_BOT_TOKEN.")
        else:
            logger.error(f"Unexpected error: {error_details}")
        
        return False

# Test function to check bot's access to the channel
def check_channel_access():
    try:
        response = client.conversations_info(channel=SLACK_CHANNEL)
        logger.info(f"Successfully accessed channel info for {SLACK_CHANNEL}")
        logger.info(f"Channel name: {response['channel']['name']}")
        return True
    except SlackApiError as e:
        logger.error(f"Error accessing channel info: {e}")
        logger.info("Attempting to join the channel...")
        return join_channel()

# Run this check when the module is imported
if check_channel_access():
    logger.info("Bot has access to the specified channel.")
else:
    logger.error("Bot does not have access to the specified channel. Please check the setup instructions.")
