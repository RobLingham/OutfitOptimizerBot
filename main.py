from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import schedule_daily_outfit_suggestion
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
try:
    app.config.from_pyfile('config.py')
except ValueError as e:
    logger.error(f"Error loading configuration: {e}")
    logger.error("Please make sure all required environment variables are set.")
    exit(1)

# Initialize and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_daily_outfit_suggestion, 'cron', hour=14, minute=7, timezone='US/Eastern', id='daily_outfit_suggestion')
scheduler.start()

@app.route('/')
def health_check():
    return "Outfit Suggestion Bot is running!", 200

@app.route('/test_outfit_suggestion')
def test_outfit_suggestion():
    logger.info("Test outfit suggestion endpoint accessed")
    schedule_daily_outfit_suggestion()
    return "Outfit suggestion test triggered. Check your Slack channel and application logs.", 200

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=5000)
