#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cx_Oracle 
from logger import *
import time


#原数据库
srcServer = "127.0.0.1"							# 连接服务器地址
srcUser = "system"										# 连接帐号
srcPassword = "Yang123456"							# 连接密码
srcDbname = "orcl"									# 数据库名称
count = 0														# 数据数量
addcount = 0												# 数据增量

#同步目标数据库
tarServer = "127.0.0.1"						# 连接服务器地址
tarUser = "system"											# 连接帐号
tarPassword = "Yang123456"								# 连接密码
tarDbname = "orcl"								# 数据库名称

#日志
logger = Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

#连接数据库
srcConn = cx_Oracle.connect("%s/%s@%s/%s" % (srcUser, srcPassword, srcServer, srcDbname))
logger.info("srcDB server=%s, user=%s, password=%s dbname=%s" % (srcServer, srcUser, srcPassword, srcDbname))

tarConn = cx_Oracle.connect("%s/%s@%s/%s" % (tarUser, tarPassword, tarServer, tarDbname))
logger.info("tarDB server=%s, user=%s, password=%s dbname=%s" % (tarServer, tarUser, tarPassword, tarDbname))

#查询数据转字典方法
def makedict(cursor):
   cols = [d[0] for d in cursor.description] 
   def createrow(*args):
       return dict(zip(cols, args))
   return createrow

#初始化数据数量count
def InitScr():
	#logger.debug("InitScr() ")
	global count
	global addcount
	with srcConn.cursor() as cursor:
		cursor.execute(' select COUNT(1) sum from Persons ')
		cursor.rowfactory = makedict(cursor)
		for row in cursor:
			count = row['SUM']

#数据同步
def SynDatas():
	#logger.debug("SynDatas() ")
	global count
	global addcount
	with srcConn.cursor() as cursor:
		cursor.execute(" select * from Persons where rownum <= :ADDCOUNT order by CREATEDATE desc ", {'ADDCOUNT':addcount})
		cursor.rowfactory = makedict(cursor)
		for row in cursor:		
			with tarConn.cursor() as tarCursor:
				#logger.debug(row)
				tarCursor.execute(' INSERT INTO Persons_his (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES (:ID_P, :LASTNAME, :FIRSTNAME, :ADDRESS, :CITY, :CREATEDATE) ', 
				(row['ID_P'],row['LASTNAME'],row['FIRSTNAME'],row['ADDRESS'],row['CITY'],row['CREATEDATE']))
				tarConn.commit()
				logger.info("syn success! CREATEDATE=%s, Name=%s" % (row['CREATEDATE'], row['LASTNAME']))
				
#判断是否有新增数据
def HaveNewDatas():
	#logger.debug("HaveNewDatas() ")
	global count
	global addcount
	with srcConn.cursor() as cursor:
		cursor.execute(' select COUNT(1) sum from Persons ')
		cursor.rowfactory = makedict(cursor)
		for row in cursor:
			if count != row['SUM']:
				addcount = row['SUM'] - count
				count = row['SUM']
				return 1;
	return 0;


#主逻辑
InitScr()
try:
	while(1):
		srcConn = cx_Oracle.connect("%s/%s@%s/%s" % (srcUser, srcPassword, srcServer, srcDbname))
		tarConn = cx_Oracle.connect("%s/%s@%s/%s" % (tarUser, tarPassword, tarServer, tarDbname))
		if 1 == HaveNewDatas():
			SynDatas()
		time.sleep(1)
except Exception as e:
	logger.error("syn error! repr(e) = %s" % (repr(e)))
finally:
	logger.info("finally!")