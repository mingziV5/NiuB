#!/usr/bin/python
#coding:utf-8
from flask import Flask, request
from . import app, jsonrpc
from auth import auth_login
import utils
import json
import time
import traceback

@jsonrpc.method('selected.get')
@auth_login
def selected(auth_info, **kwargs):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    try:
        data = request.get_json()['params']
        where = data.get('where', None)
        m_table = data.get('m_table', None)
        field = data.get('field', None)
        s_table = data.get('s_table', None)
        res = app.config['db'].get_one_result(m_table, [field], where)
        res = res[field].split(',') #eg: ['1', '2']
        result = app.config['db'].get_results(s_table, ['id', 'name', 'name_cn'])
        for x in result: #eg: [{'id':1, 'name':'sa'},{'id': 2, 'name': 'php'}]
            for r_id in res:
                if int(r_id) == int(x['id']):
                    x['selected'] = 'selected="selected"'
        utils.write_log('api').info('%s selected %s successfully' %(username, s_table))
        return json.dumps({'code': 0, 'result': result})
    except:
        utils.write_log('api').error('selected error %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'selected.get faild'})
        
