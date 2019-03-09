# pysqlSyn

## 工程简介

### python支持各类数据库数据同步

## 工程详解

- **开发环境**
	
  > Win10 64位 + Python 2.7.14

- **目录结构** 

  >--code																								程序

        |-logger.py    日志类	
        |-mysqlSyn.py    mysql数据库的数据同步
        |-oracleSyn.py    oracle数据库的数据同步
        |-sqlserverSyn.py    sqlserver数据库的数据同步
        |-sqlConn.py    各类数据库集合类
        |-allSyn.py    不同数据库之间数据同步
  >--SQL																								sql语句

        |-mysql.sql    mysql环境		
        |-oracle.sql    oracle环境		
        |-sqlserver.sql    sqlserver环境

- **注意**
	
  > oracle表名与字段名无大小写区分，字典获取字段名称均为大写  
  > mysql与sqlserver表名与字段有大小写区分，字典获取字段名称有大小写区分  

## 联系信息

> Address：     **广州**  
> Email:        [**SwimYanglin@foxmail.com**][email-addr]  
> Github:       [**github.com/HQlin**][github-site]  

[email-addr]: mailto:SwimYanglin@foxmail.com
[github-site]: https://github.com/HQlin
