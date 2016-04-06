import sys

sitepackage = "D:\home\site\wwwroot\env\Lib\site-packages"
sys.path.append(sitepackage)

import requests
import json
from azure.storage.queue import QueueService
import os

service_keys = {
    'stor_acc_name': os.environ['STOR_ACC_NAME'],
    'stor_acc_key': os.environ['STOR_ACC_KEY']
}

stor_acc_name = service_keys['stor_acc_name']
stor_acc_key = service_keys['stor_acc_key']


# storage
queue_service = QueueService(account_name=stor_acc_name, account_key=stor_acc_key)

while True:
    messages = queue_service.get_messages('taskqueue', numofmessages=16, visibilitytimeout=5*60)
    for message in messages:
        d = json.loads(message.message_text)
        mobile = d['mobile']
        image = d['image']
        odp = str(image)
        payload = {'username': 'misiek1928', 'password': '9115578493baf1483c05d05daa10eb67', 'from': 'Alert', 'to': mobile, 'message': odp}
        post = requests.post('https://api.smsapi.pl/sms.do', data=payload)
        queue_service.delete_message('taskqueue', message.message_id, message.pop_receipt)