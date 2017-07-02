#!/usr/bin/python
#coding:utf-8
from api import app
import utils

#导入自定义的参数，以字典形式返回
config = utils.get_config('api')
#导入全局变量
app.config.update(config)

if __name__ == '__main__':
    app.run(host=app.config['bind'], port=int(app.config['port']), debug=True)
