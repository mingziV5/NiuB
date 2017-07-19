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
        'method': 'servergroup.create',      
        'id': '1',
        'params': {
            'name': 'etoh_test',   
            'name_cn': 'etoh_测试主机主',
            'contacts': '万朋谁谁是', 
            'address': '中国浙江杭州',
            'comment': '备注信息'
            }
        }
    '''

    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'servergroup.delete',
        'id': '1',
        'params': {
            'where': {'id': 10}
            }
        }
    '''
 
    '''
    data = {
        'jsonrpc': '2.0',
        'method': 'servergroup.update',      
        'id': '1',
        'params': {
	    'data': {'name_cn':'update_etoh', 'comment': 'update备注'},
            'where': {'id': 11}
	    }
	}

    '''
    '''
    data = {
        'jsonrpc':'2.0',
        'method': 'servergroup.getlist',      
        'id':'1',
        'params':{
            'output':['id','name','name_cn'],
            }
        }

    '''

    data = {
        'jsonrpc':'2.0',
        'method': 'servergroup.get',
        'id':'1',
        'params':{
            'output':['id','name','name_cn'],
            'where':{'name': 'etoh_xj'}
            }
        }

    r = requests.post(url, headers=headers, json=data)
    print r.status_code
    print r.text

if __name__ == '__main__':
    rpc()    
