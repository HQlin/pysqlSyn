--���ذ�װoracle11g
http://www.ddooo.com/softdown/60921.htm#dltab

pip install cx_Oracle

--������
create table Persons(
       Id_P number(2),
       LastName VARCHAR(100),
       FirstName VARCHAR(100),
       Address VARCHAR(100),
       City VARCHAR(100),
       CREATEDATE date
       );
       
create table Persons_his(
       Id_P number(2),
       LastName VARCHAR(100),
       FirstName VARCHAR(100),
       Address VARCHAR(100),
       City VARCHAR(100),
       CREATEDATE date
       );
       
--��������
INSERT INTO Persons (Id_P, LastName, FirstName, Address, City, CREATEDATE) VALUES ('0', 'huang', 'qinglin', 'tianhe', 'guangzhou', sysdate);
commit;

--�鿴ǰ��������
select * from Persons where rownum <= 1 order by CREATEDATE desc;

--����̨����
sqlplus system/Yang123456@127.0.0.1:1521/orcl




