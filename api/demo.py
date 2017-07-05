#coding:utf-8
#unicode_literals 作用将当前某块中所有字符串转换会Unicode
from __future__ import unicode_literals
from flask import Flask. render_template, session, redirect, request
from . import app
import requests
import json
import utils

headers = {'content-type': 'application/json'}

@app.route('/')
def index():
    if session.get('author', 'nologin') == 'onlogin':
        return redirect('/login')
    return render_template('index.html', user=session.get('username'))

@app.route('/user/<htmlname>')
def user(htmlname):
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    return render_template(htmlname + '.html', user=session.get('username'))

@app.route('project/<htmlname>')
def project(htmlname):
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    return render_template(htmlname + '.html', user=session.get('username'))

@app.route('cmdb/<htmlname>')
def cmdb(htmlname):
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    return render_template(htmlname + '.html', user=session.get('username'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
