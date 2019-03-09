#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlConn import *
from logger import *
import time


#原数据库
srcDbtype = "MYSQL"		#数据库类型
srcServer = "127.0.0.1"	# 连接服务器地址
srcUser = "root"	# 连接帐号
srcPassword = "123456"	# 连接密码
srcDbname = "ORDER1"	# 数据库名称
count = 0	# 数据数量
addcount = 0	# 数据增量

#同步目标数据库
tarDbtype = "SQLSERVER"
tarServer = "127.0.0.1"
tarUser = "root"
tarPassword = "123456"
tarDbname = "ORDER"

#日志
logger = Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

#连接数据库
srcConn = SqlConn(dbtype = srcDbtype, userName = srcUser, password = srcPassword, host = srcServer, instance = srcDbname)
logger.info("srcDB type=%s, server=%s, user=%s, password=%s dbname=%s" % (srcDbtype, srcServer, srcUser, srcPassword, srcDbname))

tarConn = SqlConn(tarDbtype, tarUser, tarPassword, tarServer, tarDbname)
logger.info("tarDB type=%s, server=%s, user=%s, password=%s dbname=%s" % (tarDbtype, tarServer, tarUser, tarPassword, tarDbname))


#初始化数据数量count
def InitScr():
	logger.debug("InitScr() ")
	global count
	global addcount
	sql =  ' select COUNT(1) SUM from Persons '
	cursor = srcConn.query(sql)
	for row in cursor:
		count = row['SUM']

#数据同步
def SynDatas():
	logger.debug("SynDatas() ")
	global count
	global addcount
	sql = " select * from Persons order by CREATEDATE desc limit %s " % (addcount);
	cursor = srcConn.query(sql)
	for row in cursor:
		sql = "INSERT INTO Persons (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES ('%s', '%s', '%s', '%s', '%s', '%s') " % (row['Id_P'],row['LastName'],row['FirstName'],row['Address'],row['City'],row['CREATEDATE']);
		logger.info(sql)
		tarConn.execute(sql);
		logger.info("syn success! CREATEDATE=%s, Name=%s" % (row['CREATEDATE'], row['LastName']))

#判断是否有新增数据
def HaveNewDatas():
	logger.debug("HaveNewDatas() ")
	global count
	global addcount
	sql =  ' select COUNT(1) SUM from Persons '
	cursor = srcConn.query(sql)
	for row in cursor:
		if count != row['SUM']:
			addcount = row['SUM'] - count
			count = row['SUM']
			return 1;
	return 0;

#主逻辑
try:
	InitScr()
	while(1):
		srcConn = SqlConn(dbtype = srcDbtype, userName = srcUser, password = srcPassword, host = srcServer, instance = srcDbname)
		tarConn = SqlConn(tarDbtype, tarUser, tarPassword, tarServer, tarDbname)
		logger.info(count)
		if 1 == HaveNewDatas():
			SynDatas()
		time.sleep(1)
except Exception as e:
	logger.error("syn error! repr(e) = %s" % (repr(e)))
finally:
	logger.info("finally!")