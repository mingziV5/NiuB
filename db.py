#!/usr/bin/python
#coding:utf-8
import utils
import MySQLdb as mysql
import traceback

from DBUtils import PooledDB

class Cursor():
    def __init__(self, config):
        self.config = dict([(k[6:], config[k]) for k in config if k.startswith('mysql_')])
        if 'port' in self.config:
            self.config['port'] = int(self.config['port'])
        if 'maxcached' in self.config:
            self.config['maxcached'] = int(self.config['maxcached'])
        if 'maxconnections' in self.config:
            self.config['maxconnections'] = int(self.config['maxconnections'])
        if 'maxshared' in self.config:
            self.config['maxshared'] = int(self.config['maxshared'])
        if 'mincached' in self.config:
            self.config['mincached'] = int(self.config['mincached'])
        if self.config:
            self._connect_db()

    def _connect_db(self):
        #**self.config传入参数字典
        #self.db = mysql.connect(**self.config)
        print self.config
        self.pool = PooledDB.PooledDB(mysql, **self.config)
        self.db = self.pool.connection()
        #self.db.autocommit(True)
        #使用cursor获取操作游标
        self.cur = self.db.cursor()

    def _close_db(self):
        self.cur.close()
        self.db.close()

    def _execute(self,sql):
        try:
            return self.cur.execute(sql)
        except:
            utils.write_log('api').error('sql execute error %s' %traceback.format_exc())
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
        sql = 'INSERT INTO %s (%s) values (%s)' %(table_name, ','.join(fields), ','.join(values))
        utils.write_log('api').info('Insert sql: %s' %sql)
        return sql

    def execute_insert_sql(self, table_name, data):
        sql = self._insert_sql(table_name, data)
        if sql:
            return self._execute(sql)
        else: 
            utils.write_log('api').error('execute_insert_sql missing sql')
            return None
    
    def _select_sql(self, table_name, fields, where=None, order=None, asc_order=True, limit=None, join=False):
        if isinstance(where, dict) and where:
            conditions = []
            for k, v in where.items():
                if join and '.' in k and '.' in v:
                    conditions.append("%s=%s" %(k, v))
                elif isinstance(v, list):
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
        
    def if_id_exist(self, table_name, where, order=None, asc_order=True, limit=None, join=False):
        sql = self._select_sql(table_name, ['count(1)'], where, order, asc_order, limit, join)
        if sql:
            self._execute(sql)
            result_set = self._fetchone()
            if int(result_set[0]) == len(where['id']):
                return True
            else:
                return False
        utils.write_log('api').error('if_id_exist missing sql')
        return False
        

    def get_one_result(self, table_name, fields, where=None, order=None, asc_order=True, limit=None, join=False):
        sql = self._select_sql(table_name, fields, where, order, asc_order, limit, join)
        if sql:
            self._execute(sql)
            result_set = self._fetchone()
            if result_set:
                return dict([(k, '' if result_set[i] is None else result_set[i]) for i, k in enumerate(fields)])
            else:
                return {}
        utils.write_log('api').error('get_one_result missing sql')
        return None

    def get_results(self, table_name, fields, where=None, order=None, asc_order=True, limit=None, join=False):
        sql = self._select_sql(table_name, fields, where, order, asc_order, limit, join)
        if sql:
            self._execute(sql)
            results_all_set = self._fetchall()
            if results_all_set:
                results_list = []
                for result in results_all_set:
                    results_list.append(dict([(item, '' if result[index] is None else result[index]) for index, item in enumerate(fields)]))
                return results_list
            else:
                return {}
        utils.write_log('api').error('get_results missing sql')
        return None

    def _update_sql(self, table_name, data, where, fields=None):
        if not (where and isinstance(where, dict)):
            utils.write_log('api').error("Update error missing where conditions")
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
            utils.write_log('api').error('execute_update_sql missing sql')
            return None

    def _delete_sql(self, table_name, where):
        if not (where and isinstance(where, dict)):
            utils.write_log('api').error('Delete error missing where conditions')
            return None
        conditions = ["%s='%s'" %(k, v) for k, v in where.items()]
        sql = 'DELETE FROM %s WHERE %s' %(table_name, ' AND '.join(conditions)) 
        utils.write_log('api').info('Delete sql: %s' %sql)
        return sql

    def execute_delete_sql(self, table_name, where):
        sql = self._delete_sql(table_name, where)
        if sql:
            return self._execute(sql)
        utils.write_log('api').error('execute_delete_sql missing sql')
        return None

