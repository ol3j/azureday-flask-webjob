import requests
import json
from azure.storage.queue import QueueService
import os
import redis

service_keys = {
    'stor_acc_name': os.environ['STOR_ACC_NAME'],
    'stor_acc_key': os.environ['STOR_ACC_KEY'],
    'redis_pass': os.environ['REDIS_PASS'],
    'redis_server': os.environ['REDIS_SERVER'],
    'sms_user': os.environ['SMS_USER'],
    'sms_pass': os.environ['SMS_PASS']
}

stor_acc_name = service_keys['stor_acc_name']
stor_acc_key = service_keys['stor_acc_key']
redis_pass = service_keys['redis_pass']
redis_server = service_keys['redis_server']
sms_user = service_keys['sms_user']
sms_pass = service_keys['sms_pass']


# storage
queue_service = QueueService(account_name=stor_acc_name, account_key=stor_acc_key)

# redis
r = redis.StrictRedis(host=redis_server, port=6380, db=0, password=redis_pass, ssl=True)

while True:
    messages = queue_service.get_messages('taskqueue', numofmessages=16, visibilitytimeout=5*60)
    for message in messages:
        d = json.loads(message.message_text)
        suffix = d['suffix']
        mobile = r.get(suffix)
        image = d['image']
        odp = str(image)
        payload = {'username': sms_user, 'password': sms_pass, 'from': 'Alert', 'to': mobile, 'message': odp}
        post = requests.post('https://api.smsapi.pl/sms.do', data=payload)
        queue_service.delete_message('taskqueue', message.message_id, message.pop_receipt)