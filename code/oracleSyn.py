#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cx_Oracle 
from logger import *
import time


#ԭ���ݿ�
srcServer = "127.0.0.1"							# ���ӷ�������ַ
srcUser = "system"										# �����ʺ�
srcPassword = "Yang123456"							# ��������
srcDbname = "orcl"									# ���ݿ�����
count = 0														# ��������
addcount = 0												# ��������

#ͬ��Ŀ�����ݿ�
tarServer = "127.0.0.1"						# ���ӷ�������ַ
tarUser = "system"											# �����ʺ�
tarPassword = "Yang123456"								# ��������
tarDbname = "orcl"								# ���ݿ�����

#��־
logger = Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

#�������ݿ�
srcConn = cx_Oracle.connect("%s/%s@%s/%s" % (srcUser, srcPassword, srcServer, srcDbname))
logger.info("srcDB server=%s, user=%s, password=%s dbname=%s" % (srcServer, srcUser, srcPassword, srcDbname))

tarConn = cx_Oracle.connect("%s/%s@%s/%s" % (tarUser, tarPassword, tarServer, tarDbname))
logger.info("tarDB server=%s, user=%s, password=%s dbname=%s" % (tarServer, tarUser, tarPassword, tarDbname))

#��ѯ����ת�ֵ䷽��
def makedict(cursor):
   cols = [d[0] for d in cursor.description] 
   def createrow(*args):
       return dict(zip(cols, args))
   return createrow

#��ʼ����������count
def InitScr():
	#logger.debug("InitScr() ")
	global count
	global addcount
	with srcConn.cursor() as cursor:
		cursor.execute(' select COUNT(1) sum from Persons ')
		cursor.rowfactory = makedict(cursor)
		for row in cursor:
			count = row['SUM']

#����ͬ��
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
				
#�ж��Ƿ�����������
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


#���߼�
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