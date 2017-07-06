#!/usr/bin/python
#coding:utf-8
import os, os.path
#from os import path
import time
import json
import base64
import hashlib
import traceback
import ConfigParser
import logging,logging.config
import base64
#from logging import config

work_dir = os.path.dirname(os.path.realpath(__file__))
#获取配置文件的方法
def get_config(section=''):
    config = ConfigParser.ConfigParser()
    service_conf = os.path.join(work_dir, 'conf/service.conf')
    config.read(service_conf)

    conf_items = decrypt_config(dict(config.items('common')) if config.has_section('common') else {})
     
    #print conf_items
    if section and config.has_section(section):
        conf_items.update(config.items(section))
    return conf_items

#解密配置文件
def decrypt_config(conf_items):
    if 'mysql_passwd_encrypt' in conf_items:
        conf_items['mysql_passwd'] = base64.b64decode(conf_items.pop('mysql_passwd_encrypt'))
    if 'mysql_user_encrypt' in conf_items:
        conf_items['mysql_user'] = base64.b64decode(conf_items.pop('mysql_user_encrypt'))
    return conf_items

#写日志
def write_log(log_name):
    log_conf = os.path.join(work_dir, 'conf/logger.conf')
    logging.config.fileConfig(log_conf)
    logger = logging.getLogger(log_name)
    return logger

#加密token
def get_validate(username, uid, role, fix_pwd):
    t = int(time.time())
    return base64.b64encode('%s|%s|%s|%s|%s' %(username, t, uid, role, fix_pwd)).strip()

#解密token
def validate(key, fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    if len(x) != 5:
        write_log('api').warning('token few parameter')
        return json.dumps({'code': 1, 'errmsg': 'token few parameter'})
    if t > int(x[1]) + 2*60*60:
        write_log('api').warning('token expired')
        return json.dumps({'code': 1, 'errmsg': 'token expired'})
    if fix_pwd == x[4]:
        write_log('api').info('token right')
        return json.dumps({'code': 0, 'username': x[0], 'uid':x[2], 'r_id': x[3]})
    else:
        write_log('api').warning('token password wrong')
        return json.dumps({'code': 1, 'errmsg': 'token password wrong'})
