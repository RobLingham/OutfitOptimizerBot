from outfit_generator import generate_outfit_suggestion, parse_outfit_suggestion
from slack_bot import send_slack_message
from jinja2 import Template
import os

def schedule_daily_outfit_suggestion():
    try:
        # Generate outfit suggestion
        suggestion = generate_outfit_suggestion()
        weather, outfit, quote = parse_outfit_suggestion(suggestion)

        # Prepare message using template
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'outfit_message.txt')
        with open(template_path, 'r') as file:
            template = Template(file.read())

        message = template.render(
            weather=weather,
            outfit=outfit,
            quote=quote
        )

        # Send message to Slack
        send_slack_message(message)

    except Exception as e:
        error_message = f"Error in daily outfit suggestion: {str(e)}"
        print(error_message)
        send_slack_message(error_message)
