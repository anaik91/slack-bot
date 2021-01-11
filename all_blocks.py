def get_version():
    block = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Version 1.0.0",
				"emoji": True
			}
		}
	]
    return block

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
                    "text": "Below are the list of available commands\n• help \n • version \n • run \n • doc"
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

def get_run_help(user):
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
				"text": "Below are the list of available *run* commands\n• run lp : *List Projects*\n • run ln : *List Nodes* \n • run rc <node> : *Run Command on a Node* \n • run getjob <jobid>  : *Get Output of a JOBID*"
			}
		}
        ]
    return help_block

def get_demo(user):
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
                    "text": "*Demo Doc Block* \n`apigee-all status`\n`apigee-all verson`"
                }
            }
        ]
    return help_block

def get_error(user,message):
    block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi <@{}> \n :x: {}".format(user,message)
                }
            }
        ]
    return block

def get_command(command,output):
    block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Command `{}`Output \n```{}```".format(command,output)
                }
            }
        ]
    return block

def generic_list(data):
    block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{}".format("\n".join(data))
                }
            }
        ]
    return block

def generic_info(data):
    block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": data
                }
            }
        ]
    return block