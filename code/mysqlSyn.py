#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
from logger import *
import time


#原数据库
srcServer = "127.0.0.1"							# 连接服务器地址
srcUser = "root"										# 连接帐号
srcPassword = "123456"							# 连接密码
srcDbname = "ORDER1"									# 数据库名称
count = 0														# 数据数量
addcount = 0												# 数据增量

#同步目标数据库
tarServer = "127.0.0.1"						# 连接服务器地址
tarUser = "root"											# 连接帐号
tarPassword = "123456"								# 连接密码
tarDbname = "ORDER1"								# 数据库名称

#日志
logger = Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

#连接数据库
srcConn = pymysql.connect(srcServer, srcUser, srcPassword, srcDbname)
logger.info("srcDB server=%s, user=%s, password=%s dbname=%s" % (srcServer, srcUser, srcPassword, srcDbname))

tarConn = pymysql.connect(tarServer, tarUser, tarPassword, tarDbname) 
logger.info("tarDB server=%s, user=%s, password=%s dbname=%s" % (tarServer, tarUser, tarPassword, tarDbname))

#初始化数据数量count
def InitScr():
	global count
	global addcount
	with srcConn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
		cursor.execute(' select COUNT(1) sum from Persons ')
		for row in cursor:
			count = row['sum']

#数据同步
def SynDatas():
	global count
	global addcount
	with srcConn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
		cursor.execute(' select * from Persons order by CREATEDATE desc limit %s', addcount)
		for row in cursor:		
			with tarConn.cursor(cursor=pymysql.cursors.DictCursor) as tarCursor:
				tarCursor.execute(' INSERT INTO Persons_his (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES (%s, %s, %s, %s, %s, %s) ', (row['Id_P'],row['LastName'],row['FirstName'],row['Address'],row['City'],row['CREATEDATE']))
				tarConn.commit()
				logger.info("syn success! CREATEDATE=%s, Name=%s" % (row['CREATEDATE'], row['LastName']))
				
#判断是否有新增数据
def HaveNewDatas():
	global count
	global addcount
	with srcConn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
		cursor.execute(' select COUNT(1) sum from Persons ')
		for row in cursor:
			logger.info("syn success! %d = %d " % (count, row['sum']) )
			if count != row['sum']:
				addcount = row['sum'] - count
				count = row['sum']
				return 1;
	return 0;


#主逻辑
InitScr()
try:
	while(1):
		srcConn = pymysql.connect(srcServer, srcUser, srcPassword, srcDbname)
		tarConn = pymysql.connect(tarServer, tarUser, tarPassword, tarDbname) 
		if 1 == HaveNewDatas():
			SynDatas()
		time.sleep(1)
except Exception as e:
	logger.error("syn error! repr(e) = %s" % (repr(e)))
finally:
	logger.info("finally!")