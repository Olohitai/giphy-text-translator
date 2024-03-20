import requests
import os
from flask import jsonify
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from spellchecker import SpellChecker
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

# Initialize Slack WebClient

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
slack_client = WebClient(token=SLACK_BOT_TOKEN)
# Initialize Slack Bolt app
# bolt_app = App(token=SLACK_BOT_TOKEN)

# Download NLTK data (if not already downloaded)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# Load environment variables from .env file
load_dotenv()

# Access environment variables
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')

# Initialize the spell checker
spell_checker = SpellChecker()


def analyze_sentiment(text):
    if text is None or not text.strip():
        return jsonify({'error': 'Text parameter is missing or empty'}), 400
    # Create a TextBlob object for the input text
    blob = TextBlob(text)
    # Perform sentiment analysis and return the polarity score
    return blob.sentiment.polarity


# # Define a function for text processing and keyword extraction
def extract_keywords(text):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    # print(tokens)

    # Perform spell-checking and autocorrection
    corrected_tokens = [spell_checker.correction(token) for token in tokens]
    # Perform part-of-speech tagging to identify word types (nouns, verbs, adjectives, etc.)
    tagged_tokens = pos_tag(corrected_tokens)

    # Initialize a list to store extracted keywords
    keywords = []

    # Define the part-of-speech tags that represent nouns, verbs, and adjectives
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']  # Nouns
    verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']  # Verbs
    adjective_tags = ['JJ', 'JJR', 'JJS']  # Adjectives

    # Iterate through the tagged tokens and extract keywords based on their part-of-speech tags
    for token, tag in tagged_tokens:
        if tag in noun_tags or tag in verb_tags or tag in adjective_tags:
            # Convert to lowercase for consistency
            keywords.append(token.lower())

    # print(keywords)
    return keywords


# # Define a function to fetch GIFs from the Giphy API based on a search query
def fetch_gifs(text_message, rating='g'):
    # Perform sentiment analysis on the text message
    sentiment_score = analyze_sentiment(text_message)

    # Extract keywords from the text message
    keywords = extract_keywords(text_message)

   # Determine the sentiment label based on the sentiment score
    sentiment_label = 'happy' if sentiment_score >= 0.05 else 'sad' if sentiment_score <= - \
        0.05 else 'neutral'

    # Construct the Giphy API search query based on sentiment label and extracted keywords
    query = sentiment_label + ' ' + ' '.join(keywords)
    # Define the rating parameter for filtering out explicit content

    rating = 'g'  # Default to general audience

    print(query)

    url = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=5&rating={rating}'
    response = requests.get(url)
    data = response.json()
    # Extract GIF URLs from response
    gif_urls = [item['images']['fixed_height']['url'] for item in data['data']]

    return gif_urls


def create_modal_view(gif_urls):
    blocks = []

    # Add a header block
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Select a GIF",
            "emoji": True
        }
    })

    # Add a block for each GIF with image and button for selection
    for i, gif_url in enumerate(gif_urls):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":point_right: *GIF {i+1}*"
            },
            "accessory": {
                "type": "image",
                "image_url": gif_url,
                "alt_text": f"GIF {i+1}"
            }
        })
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Select this GIF",
                        "emoji": True,

                    },
                    "style": "primary",
                    # Include a unique value for each GIF
                    "value": json.dumps(
                        {
                            "url": gif_url,
                            "channel_id": "C06NE4NP56D"
                        }
                    ),
                    "action_id": "select_gif"


                }
            ]
        })

    # Construct the modal view payload
    modal_view = {
        "type": "modal",
        "callback_id": "your_callback_id",
        "title": {
            "type": "plain_text",
            "text": "Select GIF"
        },
        "blocks": blocks
    }

    return modal_view
