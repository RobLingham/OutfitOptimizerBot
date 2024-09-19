from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import schedule_daily_outfit_suggestion
import os
import logging
from threading import Thread
import time
import sys

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
try:
    app.config.from_pyfile('config.py')
    logger.info("Configuration loaded successfully")
except ValueError as e:
    logger.error(f"Error loading configuration: {e}")
    logger.error("Please make sure all required environment variables are set.")
    exit(1)

# Initialize and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_daily_outfit_suggestion, 'cron', hour=7, minute=30, timezone='US/Eastern', id='daily_outfit_suggestion')
scheduler.start()
logger.info("Scheduler started successfully")

@app.route('/')
def health_check():
    logger.info("Health check endpoint accessed")
    return "Outfit Suggestion Bot is running!", 200

@app.route('/test_outfit_suggestion')
def test_outfit_suggestion():
    logger.info("Test outfit suggestion endpoint accessed")
    schedule_daily_outfit_suggestion()
    return "Outfit suggestion test triggered. Check your Slack channel and application logs.", 200

def run_scheduler():
    while True:
        time.sleep(1)

def run_daily_job():
    logger.info("Running daily job")
    schedule_daily_outfit_suggestion()
    logger.info("Waiting for 2 minutes to ensure message is sent")
    time.sleep(120)  # Wait for 2 minutes
    logger.info("Daily job completed")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "daily_job":
        run_daily_job()
    else:
        logger.info("Starting Flask application and scheduler")
        Thread(target=run_scheduler).start()
        port = int(os.environ.get('PORT', 8080))
        app.run(host='0.0.0.0', port=port, debug=False)
