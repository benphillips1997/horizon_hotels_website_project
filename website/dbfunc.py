import mysql.connector
from mysql.connector import errorcode
 
hostname = "localhost"
username = "ben3phillips"
password = "Uni69Flumpyer4."
db = "ben3phillips"

def getConnection():    
    try:
        conn = mysql.connector.connect(host=hostname,                              
                              user=username,
                              password=password,
                              database=db)  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:
        return conn
