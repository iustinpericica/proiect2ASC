import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'iustin_proiect',
    password = 'iustin',
    database = 'proiect'
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for table in mycursor:
    break
else:
    mycursor.execute("CREATE TABLE FILES ( name VARCHAR(255), md5 VARCHAR(255))")
