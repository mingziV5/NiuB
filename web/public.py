#coding:utf-8
from __future__ import unicode_literals
from flask import Flask, render_template, session, redirect, request
from . import app
import requests
import json
import utils

headers = {'Content-Type': 'application/json'}
data = {
        'jsonrpc': '2.0',
        'id': 1,
    }

def get_api():
    return 'http://%s/api' %app.config['api_url']

@app.route('/listapi')
def listapi():
    headers['authorization'] = session['author']
    method = request.args.get('method')
    data['method'] = method + '.getlist'
    data['params'] = {}
    utils.write_log('web').info(data)
    r = requests.post(get_api(), headers = headers, json = data)
    utils.write_log('web').info(r.text)
    return r.text

@app.route('/addapi', methods = ['GET', 'POST'])
def addapi():
    headers['authorization'] = session['author']
    #form_data = request.form
    #print 'add---------------api %s' %form_data
    #print 'add---------------api %s' %dict(form_data)
    form_data = dict((k, ','.join(v)) for k, v in dict(request.form).items())
    #print 'add---------------api %s' %form_data
    method = form_data['method']
    data['method'] = method + '.create'
    form_data.pop('method')
    data['params'] = form_data
    utils.write_log('web').info(data)
    r = requests.post(get_api(), headers = headers, json = data)
    return r.text

@app.route('/getapi')
def getapi():
    headers['authorization'] = session['author']
    method = request.args.get('method')
    data['method'] = method + '.get'
    u_id = request.args.get('id')
    data['params'] = {
            'm_table': request.args.get('m_table', None),
            'field': request.args.get('field', None),
            's_table': request.args.get('s_table', None),
            'where': {'id': int(u_id)}
        }
    print data
    utils.write_log('web').info(data)
    r = requests.post(get_api(), headers = headers, json = data)
    return r.text

@app.route('/updateapi', methods=['GET', 'POST'])
def updateapi():
    headers['authorization'] = session['author']
    form_data = dict((k, ','.join(v)) for k, v in dict(request.form).items())
    print form_data
    method = form_data['method']
    data['method'] = method + '.update'
    form_data.pop('method')
    data['params'] = {
            'data': form_data,
            'where': {
                    'id': int(form_data['id'])
                }
        }
    print data
    utils.write_log('web').info(data)
    r = requests.post(get_api(), headers = headers, json = data)
    return r.text

@app.route('/deleteapi')
def deleteapi():
    headers['authorization'] = session['author']
    method = request.args.get('method')
    data['method'] = method + '.delete'
    data['params'] = {
            'where': {
                    'id': int(request.args.get('id'))
                }
        }
    utils.write_log('web').info(data)
    r = requests.post(get_api(), headers = headers, json = data)
    return r.text
