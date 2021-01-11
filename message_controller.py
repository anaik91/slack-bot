import shlex
from all_blocks import *
from rundeck_controller import rundeck
from flask import current_app
import logging

class messageHandler:

    def __init__(self,message,user) -> None:
        self.user=user
        self.message=message

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
        if not self.isValidMessage(self):
            return get_run_help(self.user)
        self.message=shlex.split(self.message)
        if self.message[0] == 'run':
            return self.getRunBlock(self)
        if self.message[0] == 'doc':
            return self.getDocBlock(self)
        return get_help(self.user)

    def getRunBlock(self):
        verb1 = self.message[1]
        r = rundeck(current_app.config['RUNDECK_API_URL'],current_app.config['RUNDECK_API_TOKEN'])
        if not r.isValidAuthToken():
            return get_error(self.user,'Invalid Rundeck Config')
        if len(self.message) == 1:
            if verb1 == 'lp':
                return generic_list(r.listProjects())
            else :
                return get_run_help(self.user)
        if len(self.message) == 2:
            verb2 = self.message[2:]
            if verb1 == 'ln':
                return generic_list(r.listNodes(verb2))
            elif verb1 == 'getjob':
                output=r.getJobOutput(verb2)
                return get_command('Command','\n'.join([ i['log'] for i in output ]))
            else :
                return get_run_help(self.user)
        if len(self.message) > 3:
            verb2 = self.message[2]
            verb3 = self.message[3]
            command = self.message[3:]
            if verb1 == 'rc':
                return generic_info('Job {} has been triggered'.format(r.runCommand(verb2,verb3,command)))
            else :
                return get_run_help(self.user)
        else:
            return get_run_help(self.user)
    
    def getDocBlock(self):
        return get_demo(self.user)