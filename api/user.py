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
