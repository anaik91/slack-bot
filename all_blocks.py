def get_run(user):
    block =  [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hi <@{}> \n I am Running  :runner:".format(user)
			}
		}
	]
    return block

def get_random_post(user,task,type,participants):
    block =  [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hi <@{}> , Here is an activity for you".format(user)
			}
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Task Details:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "• task : {} \n • type : {}\n • participants : {}".format(task,type,participants)
			}
		}
	]
    return block

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
                    "text": "Below are the list of available commands\n• help \n • version \n • run \n • random"
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