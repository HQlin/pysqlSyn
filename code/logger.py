#!/usr/bin/python
# -*- coding: UTF-8 -*-

#����һ����־ϵͳ�� ��Ҫ����־���������̨�� ��Ҫд����־�ļ�   
import logging

#���ֵ䱣����־����
format_dict = {
	1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
	2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
	3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
	4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
	5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}

class Logger():
	def __init__(self, logname, loglevel, logger):
		'''
			ָ��������־���ļ�·������־�����Լ������ļ�
			����־���뵽ָ�����ļ���
		'''

		# ����һ��logger
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		# ����һ��handler������д����־�ļ�
		fh = logging.FileHandler(logname)
		fh.setLevel(logging.DEBUG)

		# �ٴ���һ��handler���������������̨
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# ����handler�������ʽ
		#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		formatter = format_dict[int(loglevel)]
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		# ��logger���handler
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)


	def getlog(self):
		return self.logger