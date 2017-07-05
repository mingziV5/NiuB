#/usr/bin/python
#coding:utf-8
import requests
import json
import sys
sys.path.append('../')
import utils

headers = {'content-type': 'application/json'}

username = 'test'
password = '123456'
url = 'http://192.168.31.2:8090/api/login?username=%s&passwd=%s' %(username, password)
r = requests.get(url, headers = headers)
print r.content
result = json.loads(r.content)
print result

if result['code'] == 0:
    token = result.get('authorization')
    res = utils.validate(token, '123456')
    res = json.loads(res)
    print json.dumps({'code': 0, 'result': res})
else:
    print json.dumps({'code': 1, 'errmsg': result['errmsg']})
