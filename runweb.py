#!/usr/bin/python
#coding:utf-8
from web import app
import os,sys
import utils

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

config = utils.get_config('web')

app.config.update(config)

if __name__ == '__main__':
    app.run(host=app.config.get('bind', '0.0.0.0'), port=int(app.config.get('port')), debug=True)
