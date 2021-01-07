import os
import logging
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
count=0
# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def get_help_command(comment):
    help_text="""
    {}

    Avialable commands:
    -> help
    -> run
    -> version
    """.format(comment)

    return help_text

def process(channel,text):
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    event = payload.get("event", {})
    logging.info(event)
    channel_id = event['item']['channel']
    command_text = 'I like the Emoji. Kudos !!'
    process(channel_id,command_text)

@slack_events_adapter.on("app_mention")
def app_mention(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    blocks = event.get("blocks")
    command_text=get_help_command('Invalid Command')
    try:
        rich_text_elements = [ each_block['elements'][0]['elements'] for each_block in blocks if each_block['type'] == 'rich_text' ][0]
        command_data=rich_text_elements[-1]
        if command_data['type'] == 'user':
            process(channel_id,command_text)
            return True
        else:
            command_text=command_data['text'].strip()
    except (KeyError,IndexError):
        process(channel_id,command_text)
        return True
    logging.info(event)
    if command_text == 'help':
        process(channel_id,get_help_command('As Requested'))
    elif command_text == 'version':
        process(channel_id,'Version : 1.0.0')
    elif command_text == 'run':
        process(channel_id,'I ran')
    else:
        process(channel_id,command_text)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0',port=8080)