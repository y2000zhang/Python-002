import os

# print(os.name)
# print(os.sep)
# print(os.stat("test01.py"))
# print(os.getcwd())
import re
import requests
import json

url='https://ip.jiangxianli.com/api/proxy_ips?page=2&order_by=validated_at'
r=requests.get(url=url)
ip_dict = json.loads(r.content)
for i in ip_dict['data']['data']:
    print("'http://"+i['ip']+":"+i['port']+"',")