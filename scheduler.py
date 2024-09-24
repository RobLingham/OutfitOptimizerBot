from outfit_generator import generate_outfit_suggestion, format_outfit_suggestion
from slack_bot import send_slack_message
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

logger = logging.getLogger(__name__)

def schedule_daily_outfit_suggestion():
    try:
        logger.info("Starting daily outfit suggestion process")
        # Generate outfit suggestion
        logger.info("Calling generate_outfit_suggestion function")
        suggestion = generate_outfit_suggestion()
        logger.info("generate_outfit_suggestion function completed")

        if suggestion is None:
            error_message = "Failed to generate outfit suggestion"
            logger.error(error_message)
            send_slack_message(error_message)
            return

        logger.info("Calling format_outfit_suggestion function")
        formatted_suggestion = format_outfit_suggestion(suggestion)
        logger.info("format_outfit_suggestion function completed")

        logger.info("Outfit suggestion generated and formatted successfully")
        logger.info(f"Formatted suggestion:\n{formatted_suggestion}")

        # Add a delay before sending the message
        time.sleep(1)
        # Send message to Slack
        logger.info("Attempting to send message to Slack")
        if send_slack_message(formatted_suggestion):
            logger.info("Daily outfit suggestion sent successfully.")
        else:
            logger.error("Failed to send daily outfit suggestion.")
    except Exception as e:
        error_message = f"Error in daily outfit suggestion: {str(e)}"
        logger.error(error_message)
        send_slack_message(error_message)


# Below is the time configuration and delivery
# yeah, here. 

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        schedule_daily_outfit_suggestion,
        trigger=CronTrigger(hour=14, minute=55, timezone=timezone('US/Eastern')),
        id='daily_outfit_suggestion',
        name='Send daily outfit suggestion at 7:30 AM EST',
        replace_existing=True
    )
    scheduler.start()
    return scheduler

# For testing purposes
if __name__ == "__main__":
    schedule_daily_outfit_suggestion()