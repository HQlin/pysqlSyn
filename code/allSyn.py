#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlConn import *
from logger import *
import time


#ԭ���ݿ�
srcDbtype = "MYSQL"		#���ݿ�����
srcServer = "127.0.0.1"	# ���ӷ�������ַ
srcUser = "root"	# �����ʺ�
srcPassword = "123456"	# ��������
srcDbname = "ORDER1"	# ���ݿ�����
count = 0	# ��������
addcount = 0	# ��������

#ͬ��Ŀ�����ݿ�
tarDbtype = "SQLSERVER"
tarServer = "127.0.0.1"
tarUser = "root"
tarPassword = "123456"
tarDbname = "ORDER"

#��־
logger = Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

#�������ݿ�
srcConn = SqlConn(dbtype = srcDbtype, userName = srcUser, password = srcPassword, host = srcServer, instance = srcDbname)
logger.info("srcDB type=%s, server=%s, user=%s, password=%s dbname=%s" % (srcDbtype, srcServer, srcUser, srcPassword, srcDbname))

tarConn = SqlConn(tarDbtype, tarUser, tarPassword, tarServer, tarDbname)
logger.info("tarDB type=%s, server=%s, user=%s, password=%s dbname=%s" % (tarDbtype, tarServer, tarUser, tarPassword, tarDbname))


#��ʼ����������count
def InitScr():
	logger.debug("InitScr() ")
	global count
	global addcount
	sql =  ' select COUNT(1) SUM from Persons '
	cursor = srcConn.query(sql)
	for row in cursor:
		count = row['SUM']

#����ͬ��
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

#�ж��Ƿ�����������
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

#���߼�
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