import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SLACK_SIGNING_SECRET=os.environ["SLACK_SIGNING_SECRET"]
    SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN']
    RUNDECK_API_URL=os.environ['RUNDECK_API_URL']
    RUNDECK_API_TOKEN=os.environ['RUNDECK_API_TOKEN']