import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_jsession_id(rundeck_host,user,password):
    url = 'https://{}/j_security_check?j_username={}&j_password={}'.format(rundeck_host,user,password)
    try:
        r = requests.post(url,verify=False)
        if r.status_code == 200:
            return r
    except Exception as e:
        print(e)