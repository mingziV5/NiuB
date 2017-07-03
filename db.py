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
        if isinstance(where, dict) and where:
            conditions = []
            for k, v in where.items():
                if isinstance(v, list):
                    conditions.append('%s IN (%s)' %(k, ','.join(v)))
                elif isinstance(v, str) or isinstance(v, unicode):
                    conditions.append("%s='%s'" %(k, v))
                elif isinstance(v, int):
                    conditions.append('%s=%s' %(k, v))
            sql = 'SELECT %s FROM %s WHERE %s' %(','.join(fields), table_name, ' AND '.join(conditions))
        elif not where:
            sql = 'SELECT %s FROM %s' %(','.join(fields), table_name)
        else:
            sql = ''
        if order and (isinstance(order, str) or isinstance(order, unicode)):
            sql = '%s ORDER BY %s %s' %(sql, order, 'ASC' if asc_order else 'DESC')
        if limit and isinstance(limit, tuple) and len(limit) == 2:
            sql = '%s LIMIT %s,%s' %(sql, limit[0], limit[1])
        utils.write_log('api').info('Select sql: %s' %sql)
        return sql
        

    def get_one_result(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        sql = self._select_sql(table_name, fields, where, order, asc_order, limit)
        if sql:
            self._execute(sql)
            result_set = self._fetchone()
            if result_set:
                return dict([(k, '' if result_set[i] is None else result_set[i]) for i, k in enumerate(fields)])
            else:
                return {}
        return None

    def get_results(self, table_name, fields, where=None, order=None, asc_order=True, limit=None):
        #TODO
        return 'ok'

    def _update_sql(self, table_name, data, where, fields=None):
        if not (where and isinstance(where, dict)):
            return None
        where_cond = ["%s='%s'" %(k, v) for k, v in where.items()]
        if fields:
            conditions = ["%s='%s'" %(k, data[k]) for k in fields]
        else:
            conditions = ["%s='%s'" %(k, data[k]) for k in data]
        sql = 'UPDATE %s SET %s WHERE %s' %(table_name, ','.join(conditions), ' AND '.join(where_cond))
        utils.write_log('api').info("Update sql: %s" %sql)
        return sql

    def execute_update_sql(self, table_name, data, where, fields=None):
        sql = self._update_sql(table_name, data, where, fields)
        if sql:
            return self._execute(sql)
        else:
            return "error"

    def _delete_sql(self, table_name, where):
        #TODO
        return 'ok'

    def execute_delete_sql(self, table_name, where):
        #TODO
        return 'ok'

















