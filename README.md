# Daily Outfit Suggester Bot

This Slack bot suggests daily outfits based on weather conditions and provides inspirational quotes.

## Setup Instructions

1. Install the Slack App:
   - Go to your Slack workspace and click on "Apps" in the left sidebar.
   - Search for "Daily Outfit Suggester" and install it to your workspace.

2. Create a new Slack channel or choose an existing one where you want the bot to post messages.

3. Invite the bot to the channel:
   - In Slack, go to the channel where you want to add the bot.
   - Type `/invite @Daily Outfit Suggester` and press Enter.
   - Verify that the bot has joined the channel by checking the channel members list.

4. Get the Channel ID:
   - Right-click on the channel name in the Slack sidebar.
   - Select "Copy link" from the context menu.
   - The channel ID is the last part of the URL (e.g., C07NJLCDT8Q).

5. Update the `SLACK_CHANNEL` environment variable:
   - Go to your Replit project settings.
   - Find the "Secrets" section.
   - Add or update the `SLACK_CHANNEL` secret with the channel ID you copied in step 4.

6. Get the Bot User OAuth Token:
   - Go to your Slack App's settings page (https://api.slack.com/apps).
   - Click on your app, then navigate to "OAuth & Permissions" in the sidebar.
   - Under the "Bot Token Scopes" section, ensure that `chat:write` and `channels:join` are listed.
   - If `channels:join` is not listed, click "Add an OAuth Scope" and add it.
   - Copy the "Bot User OAuth Token" (it starts with `xoxb-`).

7. Update the `SLACK_BOT_TOKEN` environment variable:
   - In your Replit project settings, under the "Secrets" section.
   - Add or update the `SLACK_BOT_TOKEN` secret with the Bot User OAuth Token you copied.

8. Restart the Flask application:
   - In the Replit shell, run:
     ```
     pkill python
     python main.py
     ```

9. Verify bot permissions:
   - In your Slack workspace, go to the channel where you invited the bot.
   - Type `/invite @Daily Outfit Suggester` again.
   - If the bot is already in the channel, you'll see a message saying it's already there.
   - If not, the bot will be added to the channel.

## Testing the Bot

After completing the setup:

1. Access the `/test_outfit_suggestion` endpoint of your Replit application.
2. Check the Slack channel where you invited the bot. You should see a message with an outfit suggestion and an inspirational quote.

## Troubleshooting

If you encounter the "not_in_channel" error:
1. Double-check that you've invited the bot to the channel using the `/invite @Daily Outfit Suggester` command.
2. Verify that the `SLACK_CHANNEL` environment variable in your Replit secrets matches the channel ID where you invited the bot.
3. Ensure that the bot has the necessary permissions in your Slack workspace, including `chat:write` and `channels:join`.
4. Check that the `SLACK_BOT_TOKEN` is correct and starts with `xoxb-`.
5. Try removing the bot from the channel and re-inviting it.
6. Make sure the bot is actually installed in your Slack workspace. Go to your Slack App settings and check the "Install App" section to confirm it's installed.

If you continue to experience issues:
1. Check the application logs for error messages.
2. Ensure all steps have been followed correctly.
3. Verify that the bot has been added to your Slack workspace and has the required scopes (chat:write, channels:join).
4. Try creating a new Slack channel and inviting the bot to it.
5. Check if there are any Slack workspace restrictions that might prevent bots from joining channels automatically.

For any persistent issues, please contact the Slack API documentation or support for further assistance.
