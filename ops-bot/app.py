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

def process(channel,text):
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text="BOT_SENT : {}".format(text))
        assert response["message"]["text"] == " You sent : {}".format(text)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    logging.info('event ====>  {}'.format(event))
    logging.info('channel_id ====>  {}'.format(channel_id))
    logging.info('user_id ====>  {}'.format(user_id))
    logging.info('text ====>  {}'.format(text))
    if 'BOT_SENT' not in text:
        process(channel_id,text + 'User: ' + user_id)
    

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0',port=8080)
