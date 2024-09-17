from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import schedule_daily_outfit_suggestion
import os

app = Flask(__name__)

# Load configuration
try:
    app.config.from_pyfile('config.py')
except ValueError as e:
    print(f"Error loading configuration: {e}")
    print("Please make sure all required environment variables are set.")
    exit(1)

# Initialize and start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_daily_outfit_suggestion, 'cron', hour=7, minute=30, timezone='US/Eastern')
scheduler.start()

@app.route('/')
def health_check():
    return "Outfit Suggestion Bot is running!", 200

@app.route('/test_outfit_suggestion')
def test_outfit_suggestion():
    schedule_daily_outfit_suggestion()
    return "Outfit suggestion test triggered. Check your Slack channel.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
