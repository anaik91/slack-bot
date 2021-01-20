import logging
import json
from slack_bolt import App
from flask import Flask, request ,jsonify
from slack_bolt.adapter.flask import SlackRequestHandler
from config import Config
from message_controller import messageHandler
logging.basicConfig(level=logging.DEBUG)
app = App()
Config.COMMAND_LIST=json.loads(open(Config.COMMAND_LIST_FILE).read())

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
def open_modal(body,ack,shortcut, client,view):
    ack()
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
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": i
                    },
                    "value": i
                } for i in Config.COMMAND_LIST],
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
                    "text": {
                        "type": "mrkdwn",
                        "text": "Enter your own Command"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click me!"
                        },
                        "action_id": "custom_button"
                    }
                },{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Fetch Logs"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click Me",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "action_id": "log_button"
                    }
                },
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

@app.action("custom_button")
def update_modal(body,ack,shortcut, client,view):
    ack()
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
    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
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
    if 'selected_option' not in view["state"]["values"]['node_command']["node_command"].keys():
        command_value=view["state"]["values"]['node_command']["node_command"]['value']
    else:
        command_value=view["state"]["values"]['node_command']["node_command"]['selected_option']['value']
    channelid="".join(view["state"]["values"]['channel_id']["channel_id"]['selected_conversations'])
    m=messageHandler('run rc {} {}'.format(node_value.replace('#',' '),command_value),user,channelid)
    say(channel=channelid,blocks=m.getBlock())

@app.action("log_button")
def open_log_modal(body,ack,shortcut, client,view):
    ack()
    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
        "type": "modal",
        "callback_id": "get_log_view",
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
            "text": "Log Exporter",
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
                "block_id": "log_path",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "log_path"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Enter the File Path",
                    "emoji": True
                }
            },
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

@app.view("get_log_view")
def handle_log_submission(ack, body, client,say, view):
    ack()
    user = body["user"]["id"]
    node_value=view["state"]["values"]['node_ip']['node_ip']['selected_option']['value']
    log_path=view["state"]["values"]['log_path']['log_path']['value']
    channelid="".join(view["state"]["values"]['channel_id']["channel_id"]['selected_conversations'])
    command='sudo python3 /tmp/minio_client.py --minio_url {} --minio_access_key {} --minio_secret_key {} --minio_bucket {} --file_location {}'.format(Config.MINIO_URL,Config.MINIO_ACCESS_KEY,Config.MINIO_SECRET_KEY,Config.MINIO_BUCKET,log_path)
    m=messageHandler('gl {} {}'.format(' '.join(node_value.split('#')[:2]),command),user,channelid)
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