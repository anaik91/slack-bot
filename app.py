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
                    "type": "input",
                    "block_id": "command_type",
                    "element": {
                        "type": "radio_buttons",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Pre-defined Commands",
                                    "emoji": True
                                },
                                "value": "default"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Enter the Comand",
                                    "emoji": True
                                },
                                "value": "custom"
                            }
                        ],
                        "action_id": "command_type"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Run Type",
                        "emoji": True
                    }
                }
            ]
        })

@app.view("run_cmd_view")
def custom_command(body,ack,shortcut, client):
    ack()
    command_type=view["state"]["values"]['command_type']['command_type']['selected_option']['value']
    if command_type == 'default':
        command_block={
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
    else:
        command_block={
            "type": "section",
            "block_id": "node_command",
            "text": {
                "type": "mrkdwn",
                "text": "Command to Run"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "options": [{
                        "text": {
                            "type": "plain_text",
                            "text": "apigee-all status",
                            "emoji": True
                        },
                        "value": "apigee-all status"
                    }, {
                        "text": {
                            "type": "plain_text",
                            "text": "df -h",
                            "emoji": True
                        },
                        "value": "df -h"
                    }, {
                        "text": {
                            "type": "plain_text",
                            "text": "lsblk",
                            "emoji": True
                        },
                        "value": "lsblk"
                    }
                ],
                "action_id": "node_command"
            }
        }
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "custom_cmd_view",
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
                command_block,
                {
                    "type": "section",
                    "block_id": "channel_id",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Choose a Channel to Post the Output to "
                    },
                    "accessory": {
                        "type": "multi_conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select Channel",
                            "emoji": True
                        },
                        "action_id": "channel_id"
                    }
                }
            ]
        })


@app.view("custom_cmd_view")
def handle_submission(ack, body, client,say, view):
    ack()
    user = body["user"]["id"]
    node_value=view["state"]["values"]['node_ip']['node_ip']['selected_option']['value']
    command_value=view["state"]["values"]['node_command']["node_command"]['value']
    channelid="".join(view["state"]["values"]['channel_id']["channel_id"]['selected_conversations'])
    m=messageHandler('run rc {} {}'.format(node_value.replace('#',' '),command_value),user,channelid)
    say(channel=channelid,blocks=m.getBlock())

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