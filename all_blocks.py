def get_help(user):
    help_block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi <@{}> :wave:".format(user)
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "You seem to have stumbled upon our HELP doc\n"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Below are the list of avialable commands\n• help \n • version \n • run"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Great to see you here Human ! Bot helps with you day to today needs"
                }
            }
        ]
    return help_block