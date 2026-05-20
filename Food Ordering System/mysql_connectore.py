import mysql.connector as sql

connection = sql.connect(host="127.0.0.1",
                         user="root",
                         password="sairam")

cursor1 = connection.cursor()

create_db = "create database if not exists sample"
cursor1.execute(create_db)

use_qurry = "use sample"
cursor1.execute(use_qurry)

create_tb1 = 'create table if not exists random(uid int primary key,name varchar(30))'
cursor1.execute(create_tb1)


n = int(input("Enter a number:"))
name = input("Enter name")
cursor1.execute(f"insert into random values({n},'{name}')")

a = 'select * from random'
cursor1.execute(a)

for item in cursor1:
    print(item)

cursor1.execute('Commit')

connection.close()
