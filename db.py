from mysql.connector import connect

myhost = 'localhost'
mydatabase = 'company'
myuser = 'root'
mypass = ''

con = connect(host = myhost,
              database = mydatabase,
              user = myuser,
              password = mypass)

cur = con.cursor()
