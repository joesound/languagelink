import mysql.connector
from hashlib import sha256
from dotenv import load_dotenv
import os

load_dotenv()
salt = os.getenv("salt")
host = os.getenv("local_host")
account = os.getenv("local_user")
password = os.getenv("local_pass")    

mydb = mysql.connector.connect(     #登入資料庫
                host=host,
                user=account ,
                password=password ,
                database="languagelink"
                )


def create_user(users_info):
    user_email = users_info["email"]
    user_name =  users_info["name"]
    user_password = users_info["password"]
    user_password = salt + user_password
    user_password_bytes = user_password.encode('utf-8')
    user_password_hash = sha256(user_password_bytes)
    user_password_sha = user_password_hash.hexdigest()
    mycursor = mydb.cursor()
    try:
        sql = "SELECT name FROM `users` WHERE email=%s"
        val=(user_email,)
        mycursor.execute(sql.lower(), val)
        user_infor = mycursor.fetchone()
        if user_infor:
            mycursor.close
            return {"code":400, "message":{"error":True, "message":"此mail已註冊過"}}
        sql = "INSERT INTO `users` (userid, name, email, password, time) VALUES (UUID_TO_BIN(UUID(), true), %s, %s, %s, NOW())"
        # sql = "SELECT name FROM user WHERE email=%s"
        val=(user_name, user_email, user_password_sha)
        mycursor.execute(sql.lower(), val)
        # user_infor = mycursor.fetchone()
        # if user_infor:
        #     return [400, "此mail已註冊過"]
        # sql="INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
        # val=(name, email, password)
        # mycursor.execute(sql.lower(), val)
        mydb.commit()
        mycursor.close  
        return {"code":200, "message":{"ok":True}}
    except mysql.connector.Error as err:
            mycursor.close
            return {"code":500, "message":{"error":True, "message":err}}
    

def read_user(email):
    mycursor = mydb.cursor()
    try:
        sql="SELECT BIN_TO_UUID(userid), name, email, password, time FROM `users` WHERE email=%s"
        val=(email,)
        mycursor.execute(sql.lower(), val)
        user_infor = mycursor.fetchone()
        mycursor.close  
        data = {
            "userid":user_infor[0],
            "name": user_infor[1],
            "email": user_infor[2],
            "password": user_infor[3],
        }
        return {"code":200, "message":data}
    except mysql.connector.Error as err:
            mycursor.close
            return {"code":500, "message":{"error":True, "message":err}}




if __name__ == "__main__":
    userdata = {
        "email": "test@test.com",
        "name": "test",
        "password":"test"
    }
    data = create_user(userdata)
    print(data)

    data = read_user(userdata["email"])
    print(data)



