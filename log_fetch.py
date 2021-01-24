from rundeck_controller import rundeck
from config import Config
from message_controller import messageHandler

class rmp:
    def __init__(self) -> None:
        pass

    def get_modal_view(self):
        view={
            "type": "modal",
            "callback_id": "get_log_job_view",
            "title": {
                "type": "plain_text",
                "text": "Logs Fetcher",
                "emoji": True
            },
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
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "org",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "org"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Organization Name .Example validate ",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "env",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "env"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Environment Name .Example : prod ",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "block_id": "start_date",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Pick the Start Date*"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": "2021-01-01",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "start_date"
                    }
                },
                {
                    "type": "section",
                    "block_id": "start_time",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Pick the Start Time*"
                    },
                    "accessory": {
                        "type": "timepicker",
                        "initial_time": "00:00",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select time",
                            "emoji": True
                        },
                        "action_id": "start_time"
                    }
                },
                {
                    "type": "section",
                    "block_id": "end_date",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Pick the End Date*"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": "2021-01-01",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "end_date"
                    }
                },
                {
                    "type": "section",
                    "block_id": "end_time",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Pick the End Time*"
                    },
                    "accessory": {
                        "type": "timepicker",
                        "initial_time": "00:00",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select time",
                            "emoji": True
                        },
                        "action_id": "end_time"
                    }
                },
                {
                    "type": "section",
                    "block_id": "channel_id",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Choose a Channel to Post the Output to *"
                    },
                    "accessory": {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select Channel",
                            "emoji": True
                        },
                        "action_id": "channel_id"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        }
        return view