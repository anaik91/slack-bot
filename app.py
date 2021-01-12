import logging
from slack_bolt import App
from flask import Flask, request ,jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
from config import Config
from message_controller import messageHandler
logging.basicConfig(level=logging.DEBUG)
app = App()

@app.event("reaction_added")
def foo(say):
    say("I Like It !!")

@app.event("app_mention")
def event_test(body,say, ack,logger):
    ack('ack')
    logger.info(body)
    event = body.get("event", {})
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
    say(blocks=m.getBlock())

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route('/doctest/<component>/<subcommand>')
def doctest(component,subcommand):
    m=messageHandler('doc {} {}'.format(component,subcommand),'user','channel_id')
    return jsonify({'status': m.getBlock()})

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',port=8080)