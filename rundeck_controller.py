from time import sleep
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class rundeck:

    def __init__(self,baseUrl,authToken) -> None:
        self.baseUrl=baseUrl
        self.authToken=authToken
        self.headers={
        'X-Rundeck-Auth-Token': authToken,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

    def isValidAuthToken(self):
        url = '{}/system/info'.format(self.baseUrl)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def isHealthy(self):
        url = '{}/metrics/healthcheck'.format(self.baseUrl)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def listProjects(self):
        url = '{}/projects'.format(self.baseUrl)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return [i['name'] for i in response.json()]
        else:
            return []
    
    def isValidProject(self,project):
        url = '{}/project/{}'.format(self.baseUrl,project)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    def listNodes(self,project):
        url = '{}/project/{}/resources'.format(self.baseUrl,project)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    
    def isValidNode(self,project,node):
        url = '{}/project/{}/resource/{}'.format(self.baseUrl,project,node)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            return False

    def runCommand(self,project,node,command):
        url = '{}/project/{}/run/command?filter=name:{}'.format(self.baseUrl,project,node)
        payload = {
            "project":project,
            "exec":command,
            "nodeKeepgoing": True
        }
        response=requests.post(url,headers=self.headers,json=payload,verify=False)
        if response.status_code == 200:
            data=response.json()
            return data['execution']['id']
        else:
            return 'Error'
    
    def getJobState(self,jobId):
        url = '{}/execution/{}/state'.format(self.baseUrl,jobId)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            output = response.json()
            executionState = output['executionState']
            completed = output['completed']
            if completed:
                return True,executionState
            else:
                return False,None
        else:
            return False,None
    
    def getJobOutputText(self,jobId):
        url = '{}/execution/{}/output?format=text'.format(self.baseUrl,jobId)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            output = response.text
            return output
        else:
            return []
    
    def waitForJob(self,jobId):
        completed,state=self.getJobState(jobId)
        while not completed:
            completed,state=self.getJobState(jobId)
            sleep(1)
        outputText=self.getJobOutputText(jobId)
        if state == 'SUCCEEDED':
            return True,outputText
        elif state == 'FAILED':
            return False,outputText
        else:
            return False,outputText
            