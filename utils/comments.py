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


def get_comment(id):
    mycursor = mydb.cursor()
    try:
        sql = "SELECT BIN_TO_UUID(`comments`.commentid), BIN_TO_UUID(`comments`.userid), BIN_TO_UUID(`comments`.questionid), `comments`.content, `comments`.time, `users`.name FROM `comments` INNER JOIN `users` ON `comments`.userid = `users`.userid WHERE questionid = UUID_TO_BIN(%s)"
        # sql = "SELECT name FROM user WHERE email=%s"
        val=(id,)
        mycursor.execute(sql.lower(), val)
        datas = mycursor.fetchall()
        mycursor.close  
        data = {
                "data":[]
            }
        for each_data in datas:
            insert_data = { 
                "commentid": each_data[0],
                "userid": each_data[1],
                "questionid": each_data[2],
                "content": each_data[3],
                "time": str(each_data[4]),
                "username": each_data[5],
            }
            data["data"].append(insert_data)
        return {"code":200, "message":data}
    except mysql.connector.Error as err:
            mycursor.close
            return {"code":500, "message":{"error":True, "message":err}}


def create_comment(comment_info):
    user_id = comment_info["userid"]
    question_id = comment_info["questionid"]
    content = comment_info["content"]
    mycursor = mydb.cursor()
    try:
        sql="INSERT INTO `comments` (commentid, userid, questionid, content, time) VALUES (UUID_TO_BIN(UUID(), true), UUID_TO_BIN(%s), UUID_TO_BIN(%s), %s, NOW())"
        val=(user_id, question_id, content,)
        mycursor.execute(sql.lower(), val)
        mydb.commit()
        mycursor.close 
        return {"code":200, "message":{"ok":True}}
    except mysql.connector.Error as err:
            mycursor.close
            return {"code":500, "message":{"error":True, "message":err}}


if __name__ == "__main__":
    testdata = {
        'userid': '11ecd992-86c7-5e15-8830-f0761cd11ee5',
        'questionid': '11ecd99d-0125-4b7b-8830-f0761cd11ee5',
        "content":"test"
    }
    data = create_comment(testdata)
    print(data)

    data = get_comment('11ecd99d-0125-4b7b-8830-f0761cd11ee5')
    print(data)