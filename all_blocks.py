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
    block=[]
    if status:
        for each_node in output:
            if len(output[each_node]) < 2900:
                block.append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Command: `{}` Run Success on Node *{}* :gh-check-passed: \n```{}```".format(command,each_node,output[each_node])
                            }
                        })
            else:
                ind=list(range(0,len(output[each_node]),2900))
                ind.append(len(output[each_node]))
                ind_list=[(ind[ind.index(i)],ind[ind.index(i)+1]) for i in ind if ind.index(i)<len(ind)-1]
                block.append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Command: `{}` Run Success :gh-check-passed:".format(command)
                            }
                        })
                [block.append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "```{}```".format(output[each_node][i[0]:i[1]])
                            }
                        }) for i in ind_list]
            block.append({
			    "type": "divider"
		    })
    else:
        for each_node in output:
            block.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Command: `{}` Run Failed on Node *{}* :gh-check-failed: \n```{}```".format(command,each_node,output[each_node])
                        }
                    })
    if len(block) > 50:
        block=block[:49]
        block.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*-------- Truncated to Output --------*"
			}
		})
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

def get_log(url,log_path,node,status):
    if status:
        block = [
                {
                "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Click <{}| on this is link> to Download {} from {}".format(url,log_path,node)
                    }
                },
                {
                    "type": "divider"
                }
            ]
    else:
        block = [
            {
			"type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Issue fetching file {} from {} !!".format(log_path,node)
                }
            },
            {
                "type": "divider"
            }
        ]

    return block

def get_running_job(job,state):
    if state=='start':
        block = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{} Job has been triggered.".format(job)
                }
            }
            ]
    else:
        block = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{} Job is still in progress :ownid-loader: Hang tight".format(job)
                }
            }
            ]
    return block

def get_rmp_log(org,env,sd,ed,st,et,url):
    block = [
            {
            "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Below is the link to download RMP Logs from \n • ORG {} \n • ENV {} \n • Start Time {} {} \n • End Time {} {}".format(org,env,sd,st,ed,st)
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Click <{}| on this is link> to Download logs".format(url)
                }
            },
            {
                "type": "divider"
            }
        ]
    return block