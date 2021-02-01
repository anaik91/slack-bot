import os
import sys
from time import time
from datetime import datetime,timedelta
import io
import argparse
import json
from minio import Minio

def main():
    parser = argparse.ArgumentParser(description='Minio Uploader')
    parser.add_argument('--minio_url',help='Minio Endpoint',required=True)
    parser.add_argument('--minio_access_key',help='Minio Access Key',required=True)
    parser.add_argument('--minio_secret_key',help='Minio Secret Key',required=True)
    parser.add_argument('--minio_bucket',help="Minio Bucket",required=True)
    parser.add_argument('--file_location',help="Location of file to upload",required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file_location):
        print(json.dumps({'url':''}))
        sys.exit()

    mc = Minio(
        args.minio_url,
        access_key=args.minio_access_key,
        secret_key=args.minio_secret_key,
        secure=False
    )
    epoch=str(time()).split('.')[0]
    base=os.path.basename(args.file_location)
    try:
        data=open(args.file_location,'rb').read()
    except IsADirectoryError:
        print(json.dumps({'url':''}))
        sys.exit()
    filename='{}_{}'.format(epoch,base)
    mc.put_object(args.minio_bucket,filename,io.BytesIO(data),len(data))
    url=mc.presigned_get_object(args.minio_bucket,filename)
    print(json.dumps({'url':url}))

if __name__ == "__main__":
    main()