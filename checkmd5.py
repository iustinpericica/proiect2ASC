import hashlib
import os
from my_sql_init_stuff import mycursor
from my_sql_init_stuff import mydb
from rich import print

listOfInputs = []
listOfOutput = []

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def checkIfValid(file, md5Coding):
    mycursor.execute("SELECT * FROM FILES WHERE name = '{}'".format(file).replace("\\", "\\\\"))

    myresult = mycursor.fetchone()

    if not myresult:
        # notific user ca pt acest fisier nu a fost creat un md5
        listOfOutput.append("[yellow]Nu a fost creat niciun md5 pentru acest fisier pana acum ... {}\n".format(file))
        
    else:
        # exista un md5 pentru fisierul meu:
        md5file = md5(file)
        if myresult[1] != md5file:
            listOfOutput.append("[red]Md5 pentru acest fisier difera: -> {} \n  a fost: .. {} \n  acum e: .. {}\n".format(file, myresult[1], md5file))

        # sa vedem ce formatare are



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
                checkIfValid(file, md5(file))
    else:
        file = inputName
        checkIfValid(file, md5(file))

if listOfOutput:
    print(*listOfOutput)
else:
    print("[green]All is fine")

