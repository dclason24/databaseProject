#this is where we connect to database

import pymysql

dbserver1 = pymysql.connect(
    host="dbdev.cs.kent.edu",
    user= "dclason",
    password= "jlnAVs97",
    database= "dclason") #for connecting to the CS server