from flask import Flask
from scheduler import schedule_daily_outfit_suggestion, init_scheduler
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
try:
    app.config.from_pyfile('config.py')
    logger.info("Configuration loaded successfully")
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    logger.error("Please make sure all required environment variables are set.")
    exit(1)

@app.route('/')
def health_check():
    logger.info("Health check endpoint accessed")
    return "Outfit Suggestion Bot is running!", 200

@app.route('/test_outfit_suggestion')
def test_outfit_suggestion():
    logger.info("Test outfit suggestion endpoint accessed")
    schedule_daily_outfit_suggestion()
    return "Outfit suggestion test triggered. Check your Slack channel and application logs.", 200

if __name__ == "__main__":
    scheduler = init_scheduler()
    logger.info("Starting Flask application")
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080)
