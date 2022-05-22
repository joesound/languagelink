import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# host = os.getenv("aws_rds_url")
# account = os.getenv("aws_rds_user")
# password = os.getenv("aws_rds_password")    

host = os.getenv("local_host")
account = os.getenv("local_user")
password = os.getenv("local_pass")    


mydb = mysql.connector.connect(     #登入資料庫
                host= host,
                user= account,
                password= password,
                )


mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS `languagelink`")
mycursor.close()