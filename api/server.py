#coding:utf8
from flask import request
from . import app, jsonrpc
from auth import auth_login
import json
import traceback
import utils

@jsonrpc.method('server.create')
@auth_login
def server_create(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        if not data.has_key('sg_id'):
            return json.dumps({'code': 1, 'errmsg': 'no given sg_id'})
        if not app.config['db'].if_id_exist('server_group', {'id': data['sg_id']}):
            return json.dumps({'code': 1, 'errmsg': 'sg_id not exist'})
        app.config['db'].execute_insert_sql('server', data)
        utils.write_log('api').info('%s create server % success' %(username, data['host_name']))
        return json.dumps({'code': 0, 'result': 'create server %s success' %data['host_name']})
    except:
        utils.write_log('api').error('create server faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create server faild'})


@jsonrpc.method('server.delete')
@auth_login
def server_delete(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        where = data.get('where', None)
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need conditions'})
        result = app.config['db'].get_one_result('server', ['host_name'], where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'server name or id not exit'})
        app.config['db'].execute_delete_sql('server', where)
        utils.write_log('api').info('%s delete server success' %username)
        return json.dumps({'code': 0, 'result': 'delete server success'})
    except:
        utils.write_log('api').error('delete server faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'delete server faild'})

@jsonrpc.method('server.update')
@auth_login
def server_update(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']['data']
        where = request.get_json()['params']['where']
        if not data or not where:
            return json.dumps({'code': 1, 'errmsg': 'must need data or conditions'})
        result = app.config['db'].execute_update_sql('server', data, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'no data update'})
        utils.write_log('api').info('%s update server success' %username)
        return json.dumps({'code': 0, 'result': 'update server success'})
    except:
        utils.write_log('api').error('update server faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'update server fail'})

@jsonrpc.method('server.get')
@auth_login
def server_getone(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        output = ['id', 'host_name', 'name_cn', 'ip', 'account', 'admin_username', 'admin_password', 'sg_id', 'comment', 'outerip']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where', None)
        result = app.config['db'].get_one_result('server', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        sg_results = app.config['db'].get_results('server_group', ['id', 'name_cn'])
        sg_dict = dict((str(x['id']), x['name_cn']) for x in sg_results)
        print sg_dict
        print result
        sg_name = sg_dict.get(result['sg_id'])
        result['sg_id'] = sg_name
        utils.write_log('api') .info('%s select server success' %username)
        return json.dumps({'code': 0, 'result': result}) 
    except:
        utils.write_log('api').error('select server by name or id faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select server by name or id faild'})   

@jsonrpc.method('server.getlist')
@auth_login
def server_getlist(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        output = ['id', 'host_name', 'name_cn', 'ip', 'account', 'admin_username', 'admin_password', 'sg_id', 'comment', 'outerip', 'server_group.name_cn']
        data = request.get_json()['params']
        fields = data.get('output', output) 
        where = data.get('where', {})
        where['server.sg_id'] = 'server_group.id'
        join = data.get('join', False)
        results = app.config['db'].get_results('server,server_group', fields, where, join=join)
        if not results:
            return json.dumps({'code': 1, 'errmsg': 'data not exist'})
        utils.write_log('api').info('%s select server list success' %username)
        return json.dumps({'code': 0, 'result': results, 'count': len(results)})
    except:
        utils.write_log('error').error('select server list faild %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select role list fail'})


