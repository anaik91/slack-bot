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
            return list(response.json().keys())
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
        url = '{}/project/{}/run/command?filter=name%3A%20{}&filterName='.format(self.baseUrl,project,node)
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
    
    def getJobOutput(self,jobId):
        url = '{}/execution/{}/output'.format(self.baseUrl,jobId)
        response=requests.get(url,headers=self.headers,verify=False)
        if response.status_code == 200:
            output = response.json()
            entries = output['entries']
            #'\n'.join([ i['log'] for i in entries ])
            return entries
        else:
            return []