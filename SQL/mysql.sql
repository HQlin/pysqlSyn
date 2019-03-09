--启动mysql
mysqld --console

#控制台登陆数据库
mysql -u root -p;

#修改密码
alter user 'root'@'localhost' identified by '123456';

#安装模块
pip install pymysql

CREATE DATABASE ORDER1;

use order1;

CREATE TABLE IF NOT EXISTS `Persons`(
   `Id_P` INT,
   `LastName` VARCHAR(100),
   `FirstName` VARCHAR(100),
   `Address` VARCHAR(100),
   `City` VARCHAR(100),
   `CREATEDATE` DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Persons (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES ('0', 'huang', 'qinglin', 'tianhe', 'guangzhou', NOW());

show tables;

CREATE TABLE IF NOT EXISTS `Persons_his`(
   `Id_P` INT,
   `LastName` VARCHAR(100),
   `FirstName` VARCHAR(100),
   `Address` VARCHAR(100),
   `City` VARCHAR(100),
   `CREATEDATE` DATE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

select * from Persons order by CREATEDATE desc limit 1;

