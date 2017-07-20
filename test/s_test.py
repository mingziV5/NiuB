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
    #create请求
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'server.create',      
        'id': '1',
        'params': {
            'host_name': 'sxapp1',
            'name_cn': '应用服务器1',
            'ip': '10.210.92.60', 
            'account': 'wpweihu/SxYd.!@.#2013;yjg6709/SxYd.!@.#2013',
            'admin_username': 'root',
            'admin_password': 'SxYd.!@.#2012',
            'sg_id': '1',
            'comment': 'nginx,tomcat,memcached',
            'outerip': '221.142.5.225'
            }
        }
    '''
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'server.delete',
        'id': '1',
        'params': {
            'where': {'id': 6}
            }
        }

    '''
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'server.update',      
        'id': '1',
        'params': {
	    'data': {'name_cn':'应用服务器1', 'comment': 'nginx,tomcat,memcached'},
            'where': {'id': 1}
	    }
	}

    '''
    '''
    data = {
        'jsonrpc':'2.0',
        'method': 'server.getlist',      
        'id':'1',
        'params':{
            'output': ['server.id','server.host_name','server.name_cn','server_group.name_cn'],
            'join': True
            }
        }

    '''
    data = {
        'jsonrpc':'2.0',
        'method': 'server.get',
        'id':'1',
        'params':{
            'output': ['id','host_name','name_cn', 'sg_id'],
            'where': {'id': '1'},
            }
        }
    r = requests.post(url, headers=headers, json=data)
    print r.status_code
    print r.text

if __name__ == '__main__':
    rpc()    
