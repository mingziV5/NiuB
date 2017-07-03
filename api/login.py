from api import app
from flask import Flask,request
import json
import time
import utils
import traceback

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/api/login', method=['GET'])
def login():
    try:
        username = request.args.get('username', None)
        passwd = request.args.get('passwd', None)
        #passwd = hashlib.md5(passwd).hexdigest()
        if not (username and passwd):
            return json.dumps({'code': 1, 'errmsg': '提供用户名和密码'})
        result = app.config['db'].get_one_result('user', ['id', 'username', 'password', 'r_id', 'is_lock'], {'username': username})
        if not result:
            return json.dumps({'code': 1, 'errmsg': '用户不存在'})
        if result['is_lock'] == 1:
            return json.dumps({'code': 1, 'errmsg': '用户被锁定'})
        if passwd == result['password']
            data = {'last_login': time.strftime('%Y-%m-%d %H:%M:%S')}
            app.config['db'].execute_update_sql('user', data, {'username', username})
            utils.write_log('api').info("%s login sucess" %username)
            return json.dumps({'code', 0, 'authorization': 'token'})
        else:
            return json.dumps({'code', 1, 'errmsg': '密码错误'})
    except:
        utils.write_log('api').error('login error: %S' traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': '登陆失败'})
