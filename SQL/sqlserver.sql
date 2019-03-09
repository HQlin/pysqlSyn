--安装pip: 
--https://www.cnblogs.com/NanShan2016/p/5518235.html

--python连接sql server数据库实现增删改查
--https://www.cnblogs.com/malcolmfeng/p/6909293.html

#安装模块
pip install pymssql

drop TABLE Persons;

CREATE TABLE Persons
(
Id_P int,
LastName varchar(255),
FirstName varchar(255),
Address varchar(255),
City varchar(255),
CREATEDATE datetime2
)

INSERT INTO Persons (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES ('0', 'huang', 'qinglin', 'tianhe', 'guangzhou', getdate());
INSERT INTO Persons (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES ('0', 'huang', 'qinglin', 'tianhe', 'guangzhou', getdate());

select top 1 * from Persons order by CREATEDATE desc;

select * from Persons order by CREATEDATE desc;
delete Persons where Id_P = 0;

select COUNT(1) sum from Persons;
