#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cx_Oracle
import pymssql
import pymysql

#查询数据转字典方法(oracle)
def makedict(cursor):
	cols = [d[0] for d in cursor.description]
	def createrow(*args):
		return dict(zip(cols, args))
	return createrow

class SqlConn(object):
	# init methods(oracle)
	def initOracle(self,userName,password,host,instance):
		self._conn = cx_Oracle.connect("%s/%s@%s/%s" % (userName,password,host,instance))
		self.cursor = self._conn.cursor()

	# query methods(oracle)
	def queryOracle(self,sql):
		self.cursor.execute(sql)
		self.cursor.rowfactory = makedict(self.cursor)
		return self.cursor
		
	# init methods(sqlserver)
	def initSqlserver(self,userName,password,host,instance):
		self._conn = pymssql.connect(host, userName, password, instance)
		self.cursor = self._conn.cursor(as_dict=True)
		
	# init methods(MYSQL)
	def initMysql(self,userName,password,host,instance):
		self._conn = pymysql.connect(host, userName, password, instance)
		self.cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
		
	# query methods(sqlserver OR MYSQL)
	def querySqlserver(self,sql):
		self.cursor.execute(sql)
		return self.cursor

	def query(self,sql):
		if 'ORACLE' == self._dbtype:
			return self.queryOracle(sql)
		elif 'SQLSERVER' == self._dbtype:
			return self.querySqlserver(sql)
		elif 'MYSQL' == self._dbtype:
			return self.querySqlserver(sql)

	def __init__(self,dbtype,userName,password,host,instance):
		self._dbtype = dbtype
		if 'ORACLE' == self._dbtype:
			self.initOracle(userName,password,host,instance)
		elif 'SQLSERVER' == self._dbtype:
			self.initSqlserver(userName,password,host,instance)
		elif 'MYSQL' == self._dbtype:
			self.initMysql(userName,password,host,instance)

	# insert update delete methods
	def execute(self,sql):
		self.cursor.execute(sql)
		self.commit()

	# insert batch methods(oracle)
	def insertBatch(self,sql,nameParams=[]):
		"""batch insert much rows one time,use location parameter"""
		self.cursor.prepare(sql)
		self.cursor.executemany(None, nameParams)
		self.commit()

	def commit(self):
		self._conn.commit()

	def __del__(self):
		if hasattr(self,'cursor'): 
			self.cursor.close()

		if hasattr(self,'_conn'): 
			self._conn.close()
