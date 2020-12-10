import hashlib
import os
from my_sql_init_stuff import mycursor
from my_sql_init_stuff import mydb

listOfInputs = []
alterAll = False

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def checkIfInDbIfNotPutInto(file, md5Coding):
    sql = "SELECT * FROM files WHERE name ='{}'".format(file)

    #print(sql.replace("\\", "\\\\"))

    mycursor.execute(sql.replace("\\", "\\\\"))

    myresult = mycursor.fetchone()


    if not myresult:
        # inserez acest fisier in baza mea de date
        sql = "INSERT INTO files (name, md5) VALUES (%s, %s)"
        val = (file, md5Coding)
        mycursor.execute(sql, val)

        mydb.commit()
    else:
        if alterAll and myresult[1] != md5Coding:
            sql = "UPDATE files SET md5 = '{}' WHERE name ='{}'".format(md5Coding, file).replace("\\", "\\\\")
            #print(sql)
            mycursor.execute(sql)


alterAll = bool(int(input("1 for overwriting existing recordings, 0 for writing only new files\n")))

fileNameAsInput = input("Enter file with directories and files")

with open(fileNameAsInput) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       
       listOfInputs.append(line.rstrip('\n'))
       line = fp.readline()
       cnt += 1

#creez o lista cu toate locatiile date ca input

for inputName in listOfInputs:

    if (os.path.isdir(inputName)):

        for root, dirs, files in os.walk(inputName):
            for name in files:
                file = "{}\{}".format(root, name)
                checkIfInDbIfNotPutInto(file, md5(file))
    else:
        file = inputName
        checkIfInDbIfNotPutInto(file, md5(file))

