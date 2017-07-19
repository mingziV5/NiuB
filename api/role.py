#!/usr/bin/python
#coding:utf8
from flask import request
from . import app, jsonrpc
from auth import auth_login
import json
import traceback
import utils

@jsonrpc.method('role.create')
@auth_login
def role_create(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        if not data.has_key('p_id'):
            return json.dumps({'code': 1, 'errmsg': 'no given p_id'})
        if not app.config['db'].if_id_exist('power', {'id': data['p_id'].split(',')}):
            return json.dumps({'code': 1, 'errmsg': 'p_id not exist'})
        app.config['db'].execute_insert_sql('role', data)
        utils.write_log('api').info('%s create role %s success' %(username, data['name']))
        return json.dumps({'code': 0, 'result': 'create role %s success' %data['name']})
    except:
        utils.write_log('api').error('create role faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create role faild'})

@jsonrpc.method('role.delete')
@auth_login
def role_delete(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        where = data['where']
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need conditions'})
        result = app.config['db'].get_one_result('role', ['name'], where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'role name or id not exit'})
        app.config['db'].execute_delete_sql('role', where)
        utils.write_log('api').info('%s delete role success' %username)
        return json.dumps({'code': 0, 'result': 'delete role success'})
    except:
        utils.write_log('api').error('delete role faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'delete role fail'})

@jsonrpc.method('role.update')
@auth_login
def role_update(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']['data']
        where = request.get_json()['params']['where']
        if not data or not where:
            return json.dumps({'code': 1, 'errmsg': 'must need data or conditions'})
        result = app.config['db'].execute_update_sql('role', data, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'no data update'})
        utils.write_log('api').info('%s update role success' %username)
        return json.dumps({'code': 0, 'result': 'update role success'})
    except:
        utils.write_log('api').error('update role faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'delete role fail'})

@jsonrpc.method('role.get')
@auth_login
def role_getone(auth_info, **kwargs):
    username = auth_info['username']
    try:
        output = ['id', 'name', 'name_cn', 'p_id', 'info']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where', None)
        result = app.config['db'].get_one_result('role', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        
        #查询power表生成id,name字典
        power_results = app.config['db'].get_results('power', ['id', 'name'])
        power_dict = dict((str(x['id']), x['name']) for x in power_results)

        p_name = [power_dict[p_id] for p_id in result['p_id'].split(',') if p_id in power_dict]
        result['p_id'] = ','.join(p_name)
        utils.write_log('api').info('%s select role success' %username)
        return json.dumps({'code': 0, 'result': result})
    except:
        utils.write_log('api').error('select role by name or id faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select role by name or id faild'})
            
@jsonrpc.method('role.getlist')
@auth_login
def role_getlist(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        output = ['id', 'name', 'name_cn', 'p_id', 'info']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where', None)
        results = app.config['db'].get_results('role', fields, where)
        if not results:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        power_results = app.config['db'].get_results('power', ['id', 'name'])
        power_dict = dict((str(x['id']), x['name']) for x in power_results)
        
        for result in results:
            p_name = [power_dict[p_id] for p_id in result['p_id'].split(',') if p_id in power_dict]
            result['p_id'] = ','.join(p_name)
        utils.write_log('api').info('%s select role list success' %username)
        return json.dumps({'code': 0, 'result': results, 'count': len(results)})
    except:
        utils.write_log('error').errot('select role list faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select role list faild'})
