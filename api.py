from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from fetch_gif import fetch_gifs,  create_modal_view
import os
import json

import logging

# Initialize Slack Bolt app
slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN,
          signing_secret=SLACK_SIGNING_SECRET, name="Hello bot")


@app.command("/hello")
def handle_some_command(ack, body, logger):
    ack()
    print(body)


@app.command("/find-gif")
def find_gif(ack, body, client):
    ack()
    command_text = body['text']
    user_id = body['user_id']
    channel_id = body['channel_id']
    print(command_text, user_id, channel_id)
    relevant_gifs = fetch_gifs(command_text)
    # print(relevant_gifs)

    # Construct the modal view
    modal_view = create_modal_view(relevant_gifs)
    response = slack_client.views_open(
        trigger_id=body['trigger_id'],
        view=modal_view,
        user_id=user_id,
        channel_id=channel_id,
    )


@app.action("select_gif")
def handle_gif_selection(ack, body, say, client):
    ack()
    # Extract necessary information from the action payload
    value = body["actions"][0]['value']
    value = json.loads(value)
    channel_id = value["channel_id"]
    print(channel_id)
    url = value["url"]
    user_id = body["user"]["id"]

    say(
        channel=channel_id,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "From <@" + user_id + ">",
                },
            },
            {
                "type": "image",
                "title": {"type": "plain_text", "text": "Enjoy your gif"},
                "block_id": "image_selected",
                "alt_text": "selected image from Giphy.",
                "image_url": url,
            },
        ],

    )

    try:
        slack_client.views_update(
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view={"type": "modal", "callback_id": "your_callback_id",
                  "private_metadata": ""},
        )
    except Exception as e:
        print(f"Error updating view: {str(e)}")

    # # Close the modal
    slack_client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
            "type": "modal",
                    "title": {"type": "plain_text", "text": "Modal Title"},
                    "blocks": [],
                    "callback_id": "your_callback_id",
                    "private_metadata": ""
        }
    )


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == '__main__':
    main()
