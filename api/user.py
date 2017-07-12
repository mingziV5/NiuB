#!/usr/bin/python
#coding:utf-8
from flask import request
from . import app, jsonrpc
from auth import auth_login
import utils
import time
import json
import traceback
import hashlib

@jsonrpc.method('user.create')
@auth_login
def createuser(auth_info, *arg, **kwargs):
    username = auth_info['username']
    r_id = auth_info['r_id']
    if '1' not in r_id:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        if 'r_id' not in data:
            return json.dumps({'code': 1, 'errmsg': 'must need a role'})
        if not app.config['db'].if_id_exist('role', data['r_id'].split(',')):
            return json.dumps({'code': 1, 'errmsg': 'role id not exist'})
        if data['password'] != data['repwd']:
            return json.dumps({'code': 1, 'errmsg': 'password equal repwd'})
        elif len(data['password']) < 6:
            return json.dumps({'code': 1, 'errmsg': 'passwd too short'})
        else:
            data.pop['repwd']
        #data['password'] = hashlib.md5(datap['password']).hexdigest()
        data['join_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        app.config['db'].execute_insert_sql('user', data)
        utils.write_log('api').info('%s create_user %s' %(username, data['username']))
        return json.dumps({'code': 0, 'result':'create user %s success'})
    except:
        utils.write_log('api').error('create user error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create user faild'})

@jsonrpc.method('user.delete')
@auth_login
def userdelete(auth_info, **kwargs):
    username = auth_info['username']
    if '1' not in auth_info['r_id']:
        return json.dumps({'code': 1, 'errmsg': 'you have no power'})
    try:
        data = request.get_json()['params']
        where = data.get('where', None)
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need conditions'})
        result = app.config['db'].execute_delete_sql('user', where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'user not exist'})
        utils.write_log('api').info('%s delete user success' %username)
        return json.dumps({'code': 0, 'result': 'delete user success'})
    except:
        utils.write_log('api').error('delete user error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'delete user faild'})

@jsonrpc.method('user.update')
@auth_login
def userupdate(auth_info, **kwargs):
    username = auth_info['username']
    try:
        data = request.get_json()['params']
        where = data.get('where', None)
        data = data.get('data', None)
        fields = ['name', 'username', 'email', 'mobile']
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must need conditions'})
        if not app.config['db'].if_id_exist('user', where['id']):
            return json.dumps({'code': 1, 'errmsg': 'user not exist'})
        if '1' in auth_info['r_id']:
            result = app.config['db'].execute_update_sql('user', data, where)
        else:
            result = app.cinfig['db'].execute_update_sql('user', data, where, fields)
        utils.write_log('api').info('%s update user success' %username)
        return json.dumps({'code': 0, 'result': 'update user success'})
    except:
        utils.write_log('api').error('update user error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'update user faild'})

@jsonrpc.method('user.get')
@auth_login
def userinfo(auth_info, **kwargs):
    username = auth_info['username']
    try:
        output = ['id', 'username', 'name', 'email', 'mobile', 'is_lock', 'r_id']
        data = request.get_json()['params']
        fields = data.get('output', output)
        where = data.get('where', None)
        utils.write_log('api').info('user.get where = %s' %where)
        if not where:
            return json.dumps({'code': 1, 'errmsg': 'must have  conditions'})
        result = app.config['db'].get_one_result('user', fields, where)
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'user not exist'})
        utils.write_log('api').info('%s get one user info' %username)
        return json.dumps({'code': 0, 'result': result})
    except:
        utils.write_log('api').error('get users error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'get user faild'})

#获取用户具体信息，包括基本信息，所属角色，所拥有的权限，用于用户个人中心的展示和个人资料更新
@jsonrpc.method('user.getinfo')
@auth_login
def userselfinfo(auth_info, **kwargs):
    username = auth_info['username']
    fields = ['id', 'username', 'name', 'email', 'mobile', 'is_lock', 'r_id']
    try:
        user = app.config['db'].get_one_result('user', fields, where={'username': username})
        if user.get('r_id', None):
            r_id = user['r_id'].split(',')
            rids = app.config['db'].get_results('role', ['id', 'name', 'p_id'], where = {'id': r_id})
        else:
            rids = {}
        pids = []
        for x in rids:
            pids += x['p_id'].split(',')
        pids=list(set(pids)) #去重
        user['r_id'] = [x['name'] for x in rids] #将角色id转换为角色名

        if pids:
            mypids = app.config['db'].get_results('power', ['id', 'name', 'name_cn', 'url'], where={'id': pids})
            user['p_id'] = dict([(str(x['name']), dict([(k, x[k]) for k in ('name_cn', 'url')])) for x in mypids])     #返回格式：{'git':{'name_cn':'git','url':'http://git.com'},......}
        else:
            user['p_id'] = {}

        utils.write_log('api').info('%s get user self info' %username)
        return json.dumps({'code': 0, 'user': user})
    except:
        utils.write_log('api').error('get users list error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'get user self info faild'})

@jsonrpc.method('user.getlist')
@auth_login
def userlist(auth_info, **kwargs):
    username = auth_info['username']
    r_id = auth_info['r_id']
    users = []
    fields = ['id', 'username', 'name', 'email', 'mobile', 'is_lock', 'r_id']
    try:
        if '1' not in r_id:
            return json.dumps({'code': 1, 'errmsg': 'you have no power'})
        rids = app.config['db'].get_results('role', ['id', 'name'])
        rids = dict([(str(x['id']), x['name']) for x in rids])

        result = app.config['db'].get_results('user', fields)  #[{'id:1','name':'wd','r_id':'1,2,3'},{},{}]
        #查询user表中的r_id,与role表生成的字典对比，一致则将id替换为name,如，"sa,php"
        for user in result:
            user['r_id'] = ','.join([rids[x] for x in user['r_id'].split(',') if x in rids])
        utils.write_log('api').info('%s get all users' %username)
        return json.dumps({'code': 0, 'users': result, 'count': len(result)})
    except:
        utils.write_log('api').error('get users list faild: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'get user list error'})

#修改密码
@app.route('/api/password', methods=['POST'])
@auth_login
def passwd(auth_info):
    if auth_info['code'] == 1:
        return json.dumps(auth_info)
    username = auth_info['username']
    uid = int(auth_info['uid'])
    r_id = auth_info['r_id']
    try:
        data = request.get_json()
        #管理员修改用户密码，需要传入user_id,不需要输入老密码
        if '1' in r_id and data.has_key('user_id'):
            user_id = data['user_id']
            if not app.config['db'].if_id_exist('user', user_id):
                return json.dumps({'code': 1, 'errmsg': 'user not exist'})
            #password = hashlib.md5(data['password']).hexdigest()
            password = data['password']
            app.config['db'].execute_update_sql('user', {'password': password}, {'id': user_id})
        else:
            if not data.has_key('oldpassword'):
                return json.dumps({'code': 1, 'errmsg': 'need old password'})
            #oldpassword = hashlib.md5(data['oldpassword']).hexdigest()
            oldpassword = data['oldpassword']
            res = app.config['db'].get_one_result('user', ['password'], {'username': username})
            if res['password'] != oldpassword:
                return json.dumps({'code': 1, 'errmsg': 'old password wrong'})
            #password = hashlib.md5(data['password']).hexdigest()
            password = data['password']
            app.config['db'].execute_update_sql('user', {'password': password}, {'username': username})
        utils.write_log('api').info('%s update user password success' %username)
        return json.dumps({'code': 0, 'result': 'update user passwd success'})
    except:
        utils.write_log('api').error('update user password error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'update user password faild'})
