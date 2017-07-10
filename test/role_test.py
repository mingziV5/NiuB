#!/usr/bin/python
#coding:utf-8
from __future__ import unicode_literals
import json
import requests

url = 'http://127.0.0.1:8090/api'

def login(username, password):
    rep_url = '%s/login?username=%s&passwd=%s' %(url, username, password)
    r = requests.get(rep_url)
    result = json.loads(r.content)
    if result['code'] == 0:
        token = result['authorization']
        return json.dumps({'code': 0, 'token': token})
    else:
        return json.dumps({'code': 1, 'errmsg': result['errmsg']})

def rpc():
    res = login('admin', '123456')
    result = json.loads(res)
    if int(result['code']) == 0:
        token = result['token']
        headers = {'content-type': 'application/json', 'authorization': token}
    #创建角色
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'role.create',
        'id': '1',
        'params': {
            'name': 'oracle',
            'name_cn': '数据库',
            'p_id': '3,4,6,7',
            'info': '操作数据库' 
        }

    }
    '''
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'role.delete',
        'id': '1',
        'params': {
            'where': {
                'name': 'oracle'
            }
        }
    }
    '''
    '''
    data = {
            'jsonrpc':'2.0',
            'method': 'role.update', 
            'id':'1',
            'params':{
                'data':{'name_cn':'db'},
	        'where':{'id': 11}
	    }
        }
    '''
    data = {
            'jsonrpc':'2.0',
#           'method': 'role.get',
            'method': 'role.getlist',
            'id':'1',
            'params':{
#               'output':['id','name','name_cn'],
#                'where':{'id': 9}
            }
        }
    r = requests.post(url, headers=headers, json=data)
    print r.status_code
    print r.text

if __name__ == '__main__':
    rpc()    
