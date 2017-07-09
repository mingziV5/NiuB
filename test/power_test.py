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
			'jsonrpc':'2.0',
			'method': 'power.create',      
			'id':'1',
			'params':{
			  'name':'new_power2',   
			  'name_cn': '新的权限',
			  'url':'/api/new',     
			  'comment':'cdn刷新'  
			 }
		}
    '''
    '''
    data = {
			'jsonrpc':'2.0',
			'method': 'power.delete',      
			'id':'1',
			'params':{
				'where':{'id':20}
			}
	} 
    '''
    '''
    data = {
			'jsonrpc':'2.0',
			'method': 'power.update',      
			'id':'1',
			'params':{
				'data':{'name_cn':'cdntest'},
				'where':{'id':21}
			}
	}
    '''
    '''
    data = {
			'jsonrpc':'2.0',
			'method': 'power.getlist',      
			'id':'1',
			'params':{
                'output':['id','name','name_cn'],
			}
	}
    '''
    data = {
			'jsonrpc':'2.0',
			'method': 'power.get',      
			'id':'1',
			'params':{
				'output':['id','name','name_cn'],
				'where':{'name': 'cndss'}
			 }
	}
    r = requests.post(url, headers=headers, json=data)
    print r.status_code
    print r.text

if __name__ == '__main__':
    rpc()    
