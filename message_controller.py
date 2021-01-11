import logging
import shlex
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError
from all_blocks import *
from rundeck_controller import rundeck
from config import Config
# Initialize a Web API client

def process_slack_response(channel,text=None,blocks=None):
    slack_web_client = WebClient(token=Config.SLACK_BOT_TOKEN)
    try:
        response = slack_web_client.chat_postMessage(channel=channel, text=text,blocks=blocks)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"] 
        logging.error(f"Got an error: {e.response['error']}")

class messageHandler:

    def __init__(self,message,user,channel) -> None:
        self.user=user
        self.message=message
        self.channel=channel

    def isValidMessage(self):
        if len(self.message) < 2:
            return False
        else:
            return True

    def getBlock(self):
        if self.message == 'version':
            return get_version()
        if self.message == 'help':
            return get_help(self.user)
        process_slack_response(self.channel,text='Processing ...')
        self.message=shlex.split(self.message)
        if not self.isValidMessage():
            return get_run_help(self.user)
        if self.message[0] == 'run':
            return self.getRunBlock()
        if self.message[0] == 'doc':
            return self.getDocBlock()
        return get_help(self.user)

    def getRunBlock(self):
        print(self.message)
        verb1 = self.message[1]
        r = rundeck(Config.RUNDECK_API_URL,Config.RUNDECK_API_TOKEN)
        if not r.isValidAuthToken():
            return get_error(self.user,'Invalid Rundeck Config')
        if len(self.message) == 2:
            if verb1 == 'lp':
                return generic_list(r.listProjects())
            else :
                return get_run_help(self.user)
        if len(self.message) == 3:
            verb2 = self.message[2]
            if verb1 == 'ln':
                return generic_list(r.listNodes(verb2))
            else :
                return get_run_help(self.user)
        if len(self.message) > 3:
            verb2 = self.message[2]
            verb3 = self.message[3]
            command = ' '.join(self.message[4:])
            if verb1 == 'rc':
                process_slack_response(self.channel,blocks=get_running_command(command))
                jobid=r.runCommand(verb2,verb3,command)
                status,outputText=r.waitForJob(jobid)
                if status:
                    return get_command(command,status,outputText)
                else:
                    return get_command(command,status,outputText)
            else :
                return get_run_help(self.user)
        else:
            return get_run_help(self.user)
    
    def getDocBlock(self):
        return get_demo(self.user)