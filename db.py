#!/usr/bin/python
#coding:utf-8
import utils
import MySQLdb as mysql

class Cursor():
    def __init__(self, config):
        self.config = dict([(k[6:], config[k]) for k in config if k.startswith('mysql_')])
        if 'port' in self.config:
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

    def _execute(self,sql):
        try:
            return self.cur.execute(sql)
        except:
            self._close_db()
            self._connect_db()
            return self.cur.execute(sql)

    def _fetchone(self):
        return self.cur.fetchone()

    def _fetchall(self):
        return self.cur.fetchall()

    def _insert_sql(self, table_name, data):
        fields, values = [], []
        for k, v in data.items():
            fields.append(k)
            values.append("'%s'" %v)
        sql = 'INSERI INTO %s (%s) values (%s)' %(table_name, ','.join(fields), ','.join(values))
        utils.write('api').info('Insert sql: %s' %sql)
        return sql

    def execute_insert_sql(self, table_name, data):
        #TODO
        return 'ok'
    
    def _select_sql(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        #TODO
        return 'ok'

    def get_one_result(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        #TODO
        return 'ok'

    def get_results(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        #TODO
        return 'ok'

    def _update_sql(self, table_name, data, where, fields=None):
        #TODO
        return 'ok'

    def execute_update_sql(self, table_name, data, where, fields=None):
        #TODO
        return 'ok'

    def _delete_sql(self, table_name, where):
        #TODO
        return 'ok'

    def execute_delete_sql(self, table_name, where):
        #TODO
        return 'ok'

















