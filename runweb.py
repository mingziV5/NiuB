#!/usr/bin/python
#coding:utf-8
from web import app
import os,sys
import utils
#flask session key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#获取web的config配置
config = utils.get_config('web')
#将配置添加到app.config中
app.config.update(config)

if __name__ == '__main__':
    app.run(host=app.config.get('bind', '0.0.0.0'), port=int(app.config.get('port')), debug=True)
