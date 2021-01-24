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

    def runCommand(self,project,command,node=None,tags=None):
        filter='filter=name:{}'.format(node)
        if node is not None:
            filter='filter=name:{}'.format(node)
        if tags is not None:
            filter='filter=tags:{}'.format(tags)
        if tags == 'all':
            filter='filter=tags:ldap,msui,zookeeper,cassandra,router,mp,pgs,pgm,qpid'
        url = '{}/project/{}/run/command?{}'.format(self.baseUrl,project,filter)
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

    def runJob(self,jobId,options):
        url = '{}/job/{}/run'.format(self.baseUrl,jobId)
        payload = {
            "options":options
        }
        response=requests.post(url,headers=self.headers,json=payload,verify=False)
        if response.status_code == 200:
            data=response.json()
            return data['id']
        else:
            return 'Error'

    def getJobState(self,jobId):
        url = '{}/execution/{}/state'.format(self.baseUrl,jobId)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            output = response.json()
            executionState = output['executionState']
            allNodes = output['allNodes']
            completed = output['completed']
            if completed:
                return True,executionState,allNodes
            else:
                return False,None,None
        else:
            return False,None,None
    
    def getJobOutputText(self,jobId,node):
        url = '{}/execution/{}/output/node/{}?format=text'.format(self.baseUrl,jobId,node)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            output = response.text
            return output
        else:
            return []
    
    def getJobOutput(self,jobId,node):
        url = '{}/execution/{}/output'.format(self.baseUrl,jobId)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def waitForJob(self,jobId):
        completed,state,allNodes=self.getJobState(jobId)
        while not completed:
            completed,state,allNodes=self.getJobState(jobId)
            sleep(1)
        outputTexts={}
        for each_node in allNodes:
            outputTexts[each_node]=self.getJobOutputText(jobId,each_node)
        if state == 'SUCCEEDED':
            return True,outputTexts
        elif state == 'FAILED':
            return False,outputTexts
        else:
            return False,outputTexts