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
            utils.write_log('api').info("%s login sucess" %username)
            return json.dumps({'code': 0, 'authorization': 'token'})
        else:
            return json.dumps({'code': 1, 'errmsg': 'error password'})
    except:
        utils.write_log('api').error('login error: %s' %traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'login failed'})
