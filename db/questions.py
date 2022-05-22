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
                database="languagelink"
                )

#建立資料表 function 
def creat_table(table_style):
    mycursor = mydb.cursor()
    sql = "CREATE TABLE IF NOT EXISTS `languagelink`." + table_style
    print(sql)
    mycursor.execute(sql)
    mycursor.close()

#資料表style

#建立use table(id, name, email)
comment_style = "`questions`(`questionid` BINARY(16) NOT NULL PRIMARY KEY, `userid` BINARY(16) NOT NULL, `title` VARCHAR(50) NOT NULL, `content` VARCHAR(200) NOT NULL, `time` DATE NOT NULL)"

creat_table(comment_style)