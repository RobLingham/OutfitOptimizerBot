from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL

client = WebClient(token=SLACK_BOT_TOKEN)

def send_slack_message(message):
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        print(f"Message sent: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message: {e}")
