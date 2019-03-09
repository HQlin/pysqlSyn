--����mysql
mysqld --console

#����̨��½���ݿ�
mysql -u root -p;

#�޸�����
alter user 'root'@'localhost' identified by '123456';

#��װģ��
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

