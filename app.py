import os
import logging
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from all_blocks import get_help , get_random_post

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def process(channel,text=None,blocks=None):
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text=text,blocks=blocks)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    event = payload.get("event", {})
    user = event.get("user")
    logging.info(event)
    channel_id = event['item']['channel']
    command_text = 'I like the Emoji. Kudos !!'
    process(channel_id,text=command_text)

@slack_events_adapter.on("app_mention")
def app_mention(payload):
    event = payload.get("event", {})
    user = event.get("user")
    channel_id = event.get("channel")
    blocks = event.get("blocks")
    try:
        rich_text_elements = [ each_block['elements'][0]['elements'] for each_block in blocks if each_block['type'] == 'rich_text' ][0]
        command_data=rich_text_elements[-1]
        if command_data['type'] == 'user':
            process(channel_id,blocks=get_help(user))
            return True
        else:
            command_text=command_data['text'].strip()
    except (KeyError,IndexError):
        process(channel_id,blocks=get_help(user))
        return True
    logging.info(event)
    if command_text == 'help':
        process(channel_id,blocks=get_help(user))
    elif command_text == 'version':
        process(channel_id,text='Version : 1.0.0')
    elif command_text == 'run':
        process(channel_id,text='I ran')
    elif command_text == 'random':
        process(channel_id,blocks=random_post(user))
    else:
        process(channel_id,text=command_text)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0',port=8080)