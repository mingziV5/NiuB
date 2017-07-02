#!/usr/bin/python
#coding:utf-8
import utils
import MySQLdb as mysql

class Cursor():
    def __init__(self, config):
        self.config = dict([(k[6:], config[k]) for k in config if k.startswith('mysql_')])
        if 'port' in self.config
            self.config['port'] = int(self.config['port'])
        if self.config:
            self._connect_db()

    def _connect_db(self):
        self.db = mysql.connect(**self.config)
        self.db.autocommit(True)
        self.cur = self.db.cursor()

    def _close_db(self):
        self.cur.close()
        self.db.close()
