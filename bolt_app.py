import logging
from slack_bolt import App
from time import sleep
logging.basicConfig(level=logging.DEBUG)
app = App()

@app.event("reaction_added")
def foo(say):
    say("I Like It !!")

@app.event("app_mention")
def event_test(body, say, ack,logger):
    ack('ack')
    sleep(5)
    logger.info(body)
    say("Hi from Google Cloud Functions!")

from flask import Flask, request ,jsonify
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',port=8080)