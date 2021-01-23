import logging
import shlex
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError
from all_blocks import *
from rundeck_controller import rundeck
from config import Config

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
        self.message=shlex.split(self.message)
        if self.message[0] == 'run':
            return self.getRunBlock()
        if self.message[0] == 'doc':
            return self.getDocBlock()
        if self.message[0] == 'gl':
            return self.getLogBlock()
        if not self.isValidMessage():
            return get_run_help(self.user)
        return get_help(self.user)

    def getRunBlock(self):
        print(self.message)
        verb1 = self.message[1]
        r = rundeck(Config.RUNDECK_API_URL,Config.RUNDECK_API_TOKEN)
        if not r.isValidAuthToken():
            return get_error(self.user,'Invalid Rundeck Config')
        if len(self.message) == 1:
            return get_run_help(self.user)
        if len(self.message) == 2:
            if verb1 == 'lp':
                return generic_list(r.listProjects())
            if verb1 == 'lpns':
                ps=r.listProjects()
                servers=[]
                for ep in ps:
                    nodes=r.listNodes(ep)
                    servers.extend([ '{}#{}#{}'.format(ep,i,nodes[i]['tags'] if 'tags' in nodes[i].keys() else '') for i in nodes])
                return servers
            else :
                return get_run_help(self.user)
        if len(self.message) == 3:
            verb2 = self.message[2]
            if verb1 == 'ln':
                return generic_list(list(r.listNodes(verb2).keys()))
            else :
                return get_run_help(self.user)
        if len(self.message) > 3:
            verb2 = self.message[2]
            verb3 = self.message[3]
            command = ' '.join(self.message[4:])
            if verb1 == 'rc':
                process_slack_response(self.channel,blocks=get_running_command(command,verb3))
                jobid=r.runCommand(verb2,command,node=verb3)
            elif verb1 == 'rct':
                process_slack_response(self.channel,blocks=get_running_command(command,verb3))
                jobid=r.runCommand(verb2,command,tags=verb3)
            else:
                return get_run_help(self.user)
            status,outputText=r.waitForJob(jobid)
            if status:
                return get_command(command,status,outputText)
            else:
                return get_command(command,status,outputText)
        else:
            return get_run_help(self.user)
    
    def getDocBlock(self):
        blocks=get_blocks_from_file(Config.DOC_FILE)
        component=list(blocks.keys())
        sub_command=list(blocks[component[0]].keys())
        if len(self.message)==1:
            return get_doc_help(self.user,component,sub_command)
        if len(self.message)==2:
            verb1 = self.message[1]
            if verb1 not in component:
                return get_doc_help(self.user,component,sub_command)
            else:
                sub_blocks =[]
                [ sub_blocks.extend(blocks[verb1][i]) for i in blocks[verb1] ] 
                return sub_blocks
        if len(self.message)==3:
            verb1 = self.message[1]
            verb2 = self.message[2]
            if verb1 not in component or verb2 not in sub_command:
                return get_doc_help(self.user,component,sub_command)
            else:
                return blocks[verb1][verb2]
        return get_doc_help(self.user,component,sub_command)
    
    def getLogBlock(self):
        r = rundeck(Config.RUNDECK_API_URL,Config.RUNDECK_API_TOKEN)
        if not r.isValidAuthToken():
            return get_error(self.user,'Invalid Rundeck Config')
        if len(self.message) > 3:
            project = self.message[1]
            node = self.message[2]
            command = ' '.join(self.message[3:])
            log_path = command.split(' ')[-1]
            jobid=r.runCommand(project,command,node=node)
            _,outputText=r.waitForJob(jobid)
            parsed=json.loads(outputText[node])
            url=parsed['url']
            if len(url)>0:
                return get_log(url,log_path,node,True)
            else:
                return get_log(url,log_path,node,False)