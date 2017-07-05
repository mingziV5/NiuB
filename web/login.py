#coding:utf-8
from flask import Flask, request, session, render_template, redirect
from . import app
import requests
import json
import utils

headers = {'content-type': 'application/json'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        api_url = 'http://%s/api/login?username=%s&passwd=%s' %(app.config.get('api_url'), username, password)
        #请求API验证用户，验证token
        r = requests.get(api_url, headers=headers)
        result = json.loads(r.content)
        if result['code'] == 0:
            token = result['authorization']
            res = utils.validate(token, app.config.get('passport_key'))
            #return dict {'username': , 'uid': , 'r_id': }
            res = json.loads(res)
            session['author'] = token
            session['username'] = username
            return json.dumps({'code': 0})
        else:
            return json.dumps({'code': 1, 'errmsg': result['errmsg']})
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    session.pop('author', None)
    return redirect('/login')
