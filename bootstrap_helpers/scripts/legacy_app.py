import logging
import threading
from flask import Flask , jsonify
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from config import Config
from message_controller import messageHandler
from all_blocks import get_blocks_from_file
# Initialize a Flask app to host the events adapter
app = Flask(__name__)
app.doc_blocks=get_blocks_from_file(Config.DOC_FILE)
slack_events_adapter = SlackEventAdapter(Config.SLACK_SIGNING_SECRET, "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=Config.SLACK_BOT_TOKEN)

def process(channel,text,blocks):
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text=text,blocks=blocks)
        assert response["ok"]
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    event = payload.get("event", {})
    logging.info(event)
    channel_id = event['item']['channel']
    process(channel_id,'I like the Emoji. Kudos !!',None)

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
            command_text='help'
            return True
        else:
            command_text=command_data['text'].strip()
    except (KeyError,IndexError):
        command_text='help'
    logging.info(event)
    logging.info('Command: {}'.format(command_text))
    m=messageHandler(command_text,user,channel_id)
    threading.Thread(target=process, args=(channel_id,None,m.getBlock())).start()
    return 'HTTP 200 OK'

@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    logging.info(event)

@app.route('/doctest/<component>/<subcommand>')
def doctest(component,subcommand):
    m=messageHandler('doc {} {}'.format(component,subcommand),'user','channel_id')
    return jsonify({'status': m.getBlock()})

@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

@app.route('/verify')
def verify():
    process('random',text='Bot Test Check')
    try:
        response = slack_web_client.chat_postMessage(channel='random', text='Bot Test Check')
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")
        return jsonify({'status': 'Slack Test Message Sending Failed'}),502
    return jsonify({'status': 'Slack Test Message Sent'})

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0',port=8080)