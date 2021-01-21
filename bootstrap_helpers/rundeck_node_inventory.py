import sys
import os
import json

try:
    ansible_inventory=sys.argv[1]
except IndexError:
    print('Provide the location of ansible inventory')
    sys.exit()
if not os.path.exists(ansible_inventory):
    print('File : {} Does not Exist '.format(ansible_inventory))
    sys.exit()
ansible_inventory_dict=json.loads(open(ansible_inventory).read())

ssh_user='concourseci'
rundeck_inventry= {}
dcs=ansible_inventory_dict['all']['vars']['regions']

for each_group in ansible_inventory_dict['all']['children']:
    if each_group != '_meta' or each_group != 'all':
        index=1
        for each_host in ansible_inventory_dict['all']['children'][each_group]['hosts']:
            group = each_group
            for i in dcs:
                group = each_group.replace(i,'')
            rundeck_inventry[each_host] = {
                                        "osArch": "amd64",
                                        "username": ssh_user,
                                        "osFamily": "unix",
                                        "osVersion": "4.14.186-110.268.amzn1.x86_64",
                                        "nodename": each_host,
                                        "hostname": each_host,
                                        "osName": "Linux",
                                        "description": "Rundeck server node",
                                        "tags":[group,'{}-{}'.format(group,index)]
                                    }
            index+=1
        index=1
print(json.dumps(rundeck_inventry))