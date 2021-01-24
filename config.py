import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SLACK_SIGNING_SECRET=os.environ["SLACK_SIGNING_SECRET"]
    SLACK_BOT_TOKEN=os.environ['SLACK_BOT_TOKEN']
    RUNDECK_API_URL=os.environ['RUNDECK_API_URL']
    RUNDECK_API_TOKEN=os.environ['RUNDECK_API_TOKEN']
    RUNDECK_LOG_JOB_ID='4b253982-2eba-4f2d-97d2-7a8a7b265a2d'
    DOC_FILE='command-block-map.json'
    COMMAND_LIST_FILE='command_list.json'
    COMMAND_LIST=[]
    MINIO_URL='52.155.165.39:9000'
    MINIO_ACCESS_KEY='DIT3KFnTnKxXLdh3SvRT'
    MINIO_SECRET_KEY='s0eaisq4Ng7revPaKXMhkms7Y47t3DWxkpWCBSK4'
    MINIO_BUCKET='logs'
    RUNDECK_SSH_USER='concourseci'
    RUNDECK_SSH_PRIVATE_KEY='/etc/ansible/priv'