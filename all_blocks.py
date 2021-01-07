def get_random_post(user):
    block =  [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hi <@{}> :innocent: \nThe Lorem Ipsum for photos.".format(user)
			},
			"accessory": {
				"type": "image",
				"image_url": "https://picsum.photos/200/300",
				"alt_text": "photo"
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