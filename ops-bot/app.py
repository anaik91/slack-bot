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
help_text="""
Invalid Command.

Avialable commands:
-> help
-> run
-> version
"""

def process(channel,text):
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text="BOT RECEIVED : {}".format(text))
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")

@slack_events_adapter.on("app_mention")
def app_mention(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    blocks = event.get("blocks")
    command_text=help_text
    try:
        rich_text_elements = [ each_block['elements'][0]['elements'] for each_block in blocks if each_block['type'] == 'rich_text' ][0]
        command_data=rich_text_elements[-1]
        if command_data['type'] == 'user':
            process(channel_id,help_text)
            return True
        else:
            command_text=command_data['text'].strip()
    except (KeyError,IndexError):
        process(channel_id,help_text)
        return True
    logging.info(event)
    if command_text == 'help':
        process(channel_id,help_text)
    else:
        process(channel_id,command_text)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0',port=8080)