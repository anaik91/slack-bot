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
def event_test(body,say, ack,logger,client):
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

@app.shortcut("run_command_callback")
def open_modal(ack, shortcut, client):
    ack()
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "run_cmd_view",
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "title": {
                "type": "plain_text",
                "text": "Run Command Menu",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "block_id": "node_ip",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Pick a Server from the list"
                    },
                    "accessory": {
                        "action_id": "node_ip",
                        "type": "external_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item"
                        },
                        "min_query_length": 2
                    }
                },
                {
                    "type": "input",
                    "block_id": "node_command",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "node_command"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Command to Run",
                        "emoji": True
                    }
                }
            ]
        })

@app.view("run_cmd_view")
def handle_submission(ack, body, client,say, view):
    ack()
    user = body["user"]["id"]
    #node_block=[ each_block['block_id'] for each_block in view['blocks'] if each_block['type'] == 'input' and each_block['element']['action_id'] == 'node_ip' ][0]
    #command_block=[ each_block['block_id'] for each_block in view['blocks'] if each_block['type'] == 'input' and each_block['element']['action_id'] == 'node_command' ][0]
    node_value=view["state"]["values"]['node_ip']['node_ip']['selected_option']['value']
    command_value=view["state"]["values"]['node_command']["node_command"]['value']
    m=messageHandler('run rc {} {}'.format(node_value.replace('#',' '),command_value),user,user)
    say(channel=user,blocks=m.getBlock())

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route('/doctest/<component>/<subcommand>')
def doctest(component,subcommand):
    m=messageHandler('doc {} {}'.format(component,subcommand),'user','channel_id')
    return jsonify({'status': m.getBlock()})

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/slack/options", methods=["POST"])
def slack_option_list():
    m=messageHandler('run lpns','user','user')
    response = [{
      "text": {
        "type": "plain_text",
        "text": "*{}*".format(i)
      },
      "value": i
    } for i in m.getBlock()] 
    return jsonify({ "options": response })

@flask_app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',port=8080)