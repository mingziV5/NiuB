#coding:utf8
from flask import request
from . import app, jsonrpc
from auth import auth_login
import json
import traceback
import utils

@jsonrpc.method('servergroup.create')
@auth_login
def servergroup_create(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        app.config['db'].execute_insert_sql('server_group', data)
        utils.write_log('api').info('%s create serverGroup %s success' %(username, data['name']))
        return json.dumps({'code': 0, 'result': 'create %s success' %data['name']})
    except:
        utils.write_log('api').error('create serverGroup error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create serverGroup faild'})

@jsonrpc.method('servergroup.delete')
@auth_login
def servergroup_delete(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        where = data.get('where', None)
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need conditions'})
        result = app.config['db'].get_one_result('server_group', ['name'], where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'group name or id not exist'})
        app.config['db'].execute_delete_sql('server_group', where)
        utils.write_log('api').info('%s delete server_group success' %username)
        return json.dumps({'code': 0, 'result': 'delete server_group success'})
    except:
        utils.write_log('api').error('delete server_group: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'delete server_group faild'})

@jsonrpc.method('servergroup.update')
@auth_login
def servergroup_update(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params'].get('data', None)
        where = request.get_json()['params'].get('where', None)
        if not data or not where:
            return json.dumps({'code': 1, 'errmsg': 'must need data or conditions'})
        result = app.config['db'].execute_update_sql('server_group', data = data, where = where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'no data update'})
        utils.write_log('api').info('%s update server_group success' %username)
        return json.dumps({'code': 0, 'result': 'update success'})
    except:
        utils.write_log('api').error('update server_group error %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'update server_group faild'})

@jsonrpc.method('servergroup.getlist')
@auth_login
def servergroup_getlist(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        output = ['id', 'name', 'name_cn', 'contacts', 'address', 'comment']
        data = request.get_json()['params']
        fields = data.get('output', output) 
        where = data.get('where', None)
        result = app.config['db'].get_results('server_group', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        utils.write_log('api').info('%s select server_group list success' %username)
        return json.dumps({'code': 0, 'result': result, 'count': len(result)})
    except:
        utils.write_log('api').error('get list server_group error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'get server_group list faild'})

@jsonrpc.method('servergroup.get')
@auth_login
def servergroup_get(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        output = ['id', 'name', 'name_cn', 'contacts', 'address', 'comment']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where', None)
        result = app.config['db'].get_one_result('server_group', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        utils.write_log('api').info('%s select server group by id or name success' %username)
        return json.dumps({'code': 0, 'result': result})
    except:
        utils.write_log('api').error('get server group by id or name error %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'get server group by id or name'})
 
