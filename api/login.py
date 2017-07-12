#coding:utf8
from api import app
from flask import Flask,request
import json
import time
import utils
import traceback

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/api/login', methods=['GET'])
def login():
    try:
        username = request.args.get('username', None)
        passwd = request.args.get('passwd', None)
        #passwd = hashlib.md5(passwd).hexdigest()
        if not (username and passwd):
            return json.dumps({'code': 1, 'errmsg': 'no password or username'})
        result = app.config['db'].get_one_result(table_name='user', fields=['id', 'username', 'password', 'r_id', 'is_lock'], where={'username': username})
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'user not exist'})
        if result['is_lock'] == 1:
            return json.dumps({'code': 1, 'errmsg': 'user is locked'})
        if passwd == result['password']:
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            app.config['db'].execute_update_sql(table_name='user', data=data, where={'username': username})
            token = utils.get_validate(result['username'], result['id'], result['r_id'], app.config['passport_key'])
            utils.write_log('api').info("%s login sucess" %username)
            return json.dumps({'code': 0, 'authorization': token})
        else:
            return json.dumps({'code': 1, 'errmsg': 'error password'})
    except:
        utils.write_log('api').error('login error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'login failed'})

'''
@app.route('/test/insert')
def test_insert():
    data = {
        'username': 'test1', 
        'password': '123456', 
        'name': 'test_name', 
        'email': 'ming_v5@163.com', 
        'mobile': '88888888888', 
        'r_id': 0,
        'is_lock': 1, 
        'join_date': '2017-07-05 15:18:32'
        }
    insert_result = app.config['db'].execute_insert_sql(table_name='user', data=data)
    print insert_result
    return 'test'

@app.route('/test/select')
def  test_select():
    select_result = app.config['db'].get_one_result(table_name='user', fields=['id', 'username'], where={'username': 'test'})
    select_result_all = app.config['db'].get_results(table_name='user', fields=['id', 'username'], where={'r_id': 0})
    print select_result
    print select_result_all
    return 'test'

@app.route('/test/update')
def test_update():
    data = {'username': 'test_update'}
    update_result = app.config['db'].execute_update_sql(table_name='user', data=data, where={'username': 'test2'})
    print update_result
    return 'test'

@app.route('/test/delete')
def test_delete():
    del_result = app.config['db'].execute_delete_sql(table_name='user', where={'username': 'test_update'})
    print del_result
    return 'test'
'''
