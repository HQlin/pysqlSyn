--���ذ�װoracle11g
http://www.ddooo.com/softdown/60921.htm#dltab

pip install cx_Oracle

--������
CREATE TABLE PERSONS(
       ID_P NUMBER(2),
       LASTNAME VARCHAR(100),
       FIRSTNAME VARCHAR(100),
       ADDRESS VARCHAR(100),
       CITY VARCHAR(100),
       CREATEDATE DATE
       );
       
CREATE TABLE PERSONS_HIS(
       ID_P NUMBER(2),
       LASTNAME VARCHAR(100),
       FIRSTNAME VARCHAR(100),
       ADDRESS VARCHAR(100),
       CITY VARCHAR(100),
       CREATEDATE DATE
       );
       
--��������
INSERT INTO PERSONS (ID_P, LASTNAME, FIRSTNAME, ADDRESS, CITY, CREATEDATE) VALUES ('0', 'HUANG', 'QINGLIN', 'TIANHE', 'GUANGZHOU', SYSDATE);
COMMIT;

--�鿴ǰ��������
SELECT * FROM PERSONS WHERE ROWNUM <= 1 ORDER BY CREATEDATE DESC;

--����̨����
sqlplus system/Yang123456@127.0.0.1:1521/orcl




