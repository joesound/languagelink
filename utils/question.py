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


def create_question(questions_info):
    user_id = questions_info["userid"]
    title = questions_info["title"]
    content = questions_info["content"]
    print(user_id,title, content,)
    mycursor = mydb.cursor()
    try:
        sql="INSERT INTO `questions` (questionid, userid, title, content, time) VALUES (UUID_TO_BIN(UUID(), true), UUID_TO_BIN(%s), %s, %s, NOW())"
        val=(user_id,title, content,)
        mycursor.execute(sql.lower(), val)
        mydb.commit()
        mycursor.close 
        return {"code":200, "message":{"ok":True}}
    except mysql.connector.Error as err:
            mycursor.close
            return {"code":500, "message":{"error":True, "message":err}}

def get_question(page):
    mycursor = mydb.cursor()
    try:
        low_limit = int(page) * 12
        sql = "SELECT  BIN_TO_UUID(q.questionid) , BIN_TO_UUID(q.userid), q.title, q.content, q.time, u.name FROM `questions` AS q, `users` AS u WHERE q.userid = u.userid LIMIT %s,13;"
        val=(low_limit,)
        mycursor.execute(sql.lower(), val)
        datas = mycursor.fetchall()
        if len(datas) > 12:
            data = {
                "nextPage": page+1,
                "data":[]
                
            }
            datas = datas[0:12]
        elif len(datas) <= 12 and len(datas)>0:
            data = {
                "nextPage": None,
                "data":[]
            }
        else:
            data = {
                "nextPage": None,
                "data":[]
            }
            return {"code":200, "message":data}

        for each_data in datas:
            insert_data = { 
                "questionid": each_data[0],
                "userid": each_data[1],
                "title": each_data[2],
                "content": each_data[3],
                "time": str(each_data[4]),
                "username": each_data[5],
            }
            data["data"].append(insert_data)
        mycursor.close  
        return {"code":200, "message":data}
    except mysql.connector.Error as err:
        mycursor.close
        return {"code":500, "message":{"error":True, "message":err}}



def delete_question(id):
    pass

def update_question(id):
    pass



if __name__ == "__main__":
    testdata = {
        'userid': '11ecd992-86c7-5e15-8830-f0761cd11ee5',
        "title": "test",
        "content":"test"
    }
    # data = create_question(testdata)
    # print(data)

    data = get_question(page=0)
    print(data)