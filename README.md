# Slack GIF Bot

The Slack GIF Bot is a Python application built with the Slack Bolt framework and Giphy API integration. It enables users to search for GIFs directly within Slack, adding a fun and interactive element to conversations

## Purpose
This project aims to make it easier for users to find and share GIFs within Slack channels. With Giphy API integration, users can search for GIFs using keywords and sentiments, making conversations more engaging and dynamic.

## Features

- **GIF Search**: Users can search for GIFs using slash commands or interactive shortcuts.
- **Sentiment Analysis**: The bot performs sentiment analysis on user input to tailor GIF suggestions based on the mood of the conversation.
- **Keyword Extraction**: Relevant keywords are extracted from user messages to refine GIF search results.
- **Modal Interface**: GIF search results are displayed in a modal interface within Slack, making it easy for users to select and share GIFs.


## Prerequisites

### Slack Related Prerequisites

1. **Create a New Application:**
   - Create a new application [here](https://api.slack.com/apps).

2. **Enable Events:**
   - Go to your application and navigate to the "Event Subscriptions" tab.
   - Set "Enable Events" to On.
   - Click on "Subscribe to bot events"
   - Add the following events to subscribe to:
     - `app_home_opened`
     - `app_mention`
     - `message.channels`
     - `message.groups`
     - `message.im`
     
3. **Create a Slash Command:**
   - Go to the "Slash Commands" tab.
   - Press the "Create New Command" button.
   - Set `/find-gif` as the command and add a short description.


### Python Related Prerequisites

1. **Install Python:**
   - Make sure you have Python 3.6 or higher installed on your system.

2. **Create a Virtual Environment:**
   - Run the following command to create a virtual environment:
     ```
     python3 -m virtualenv venv
     ```

3. **Activate Virtual Environment and Install Requirements:**
   - Activate the virtual environment and install the required dependencies by running:
     ```
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Create .env File:**
   - For `SLACK_SIGNING_SECRET`, go to the "Basic Information" tab of your Slack application and copy the Signing Secret.
   - For `SLACK_APP_TOKEN`, go to the "Install App" tab, generate a token with the `connections:write` scope, and copy it.
   - For `SLACK_BOT_TOKEN`, copy the Bot User OAuth Token from the "Install App" tab of your Slack application.
   - For `GIPHY_API_KEY`, create an account on [Giphy](https://developers.giphy.com/dashboard/) and obtain an API key.
   
## Usage

Once the prerequisites are set up, activate the virtual environment (if not already activated) and start the application:

```bash
source venv/bin/activate
python api.py
```



## Usage
Once the bot is running, users can interact with it in Slack by typing commands such as /find-gif followed by keywords to search for GIFs. The bot will respond with a modal containing maximum of 5 GIF search results, allowing users to select and share GIFs in their conversations.