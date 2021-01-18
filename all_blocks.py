import json

def get_blocks_from_file(file):
    data=json.loads(open(file).read())
    return data

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
				"text": "Below are the list of available *run* commands\n• run lp \t\t\t\t\t\t\t\t\t\t: *List Projects*\n • run ln <project>    \t\t\t\t\t: *List Nodes* \n • run rc <node> <command> \t: *Run Command on a Node*"
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

def get_command(command,status,output):
    if status:
        if len(output) < 2900:
            block = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Command: `{}` Run Success :gh-check-passed: \n```{}```".format(command,output)
                        }
                    }
                ]
        else:
            ind=list(range(0,len(output),2900))
            ind.append(len(output))
            ind_list=[(ind[ind.index(i)],ind[ind.index(i)+1]) for i in ind if ind.index(i)<len(ind)-1]
            block = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Command: `{}` Run Success :gh-check-passed:".format(command)
                        }
                    }
                ]
            [block.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "```{}```".format(output[i[0]:i[1]])
                        }
                    }) for i in ind_list]
            return block
    else:
        block = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Command: `{}` Run Failed :gh-check-failed: \n```{}```".format(command,output)
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
                    "text": "* {}".format("\n* ".join(data))
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

def get_running_command(command,node):
    block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Running Command `{}` on Node `{}` :loading:".format(command,node)
                }
            }
        ]
    return block

def get_doc_help(user,component,sub_command):
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
                    "text": "*Component*\n* {}".format("\n* ".join(component))
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Sub-Command*\n* {}".format("\n* ".join(sub_command))
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Syntax*:\n`doc <component> <subcommand>`\n*Example*\n`doc cs install` OR `doc ld service` "
                }
            }
        ]
    return help_block