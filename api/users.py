from urllib import response
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, make_response
import json



app_api_users = Blueprint('users', __name__, url_prefix='/api')



request_url = "http://localhost:3000"

@app_api_users.route("/user", methods=['GET','POST','DELETE','PATCH', 'OPTIONS'])
def user_api():
    if request.method == "GET":
        user_JWT = request.cookies.get('user_token')
        if user_JWT == None:
            response = make_response(json.dumps({"data":None}))
            response.headers['Access-Control-Allow-Origin']=request_url
            response.headers['Access-Control-Allow-Credentials']= "true"
            return response
        decoded_user_JWT = decode_user_JWT(user_JWT)
        user_name = decoded_user_JWT["name"]
        user_info = get_user_by_name(user_name)
        response = make_response(json.dumps(user_info))
        response.headers['Access-Control-Allow-Origin']=request_url
        response.headers['Access-Control-Allow-Credentials']= "true"
        return response

    

    if request.method == "POST":
        # request_url = request.headers['Origin']
        creat_user_data = json.loads(request.data)
        name = creat_user_data["name"]
        email = creat_user_data["email"]
        password = creat_user_data["password"]
        print(creat_user_data)
        code, message = creat_user_check(name, email, password)
        if code == 200:
            get_user_JWT = creat_user_JWT(name, email)
            response = make_response(json.dumps(message))
            response.set_cookie(key='user_token', value=get_user_JWT, expires=time.time()+6*60)
            response.headers['Access-Control-Allow-Origin']=request_url
            response.headers['Access-Control-Allow-Credentials']= "true"
            print(response)
            return response
        else:
            response = make_response(json.dumps(message))
            response.headers['Access-Control-Allow-Origin']=request_url
            response.headers['Access-Control-Allow-Credentials']= "true"
            return response

    if request.method == "DELETE":
        # request_url = request.headers['Origin']
        message = {"ok":True}
        response = make_response(json.dumps(message))
        response.set_cookie(key='user_token', value='', expires=0)
        response.headers['Access-Control-Allow-Origin']=request_url
        response.headers['Access-Control-Allow-Credentials']= "true"
        response.headers['Access-Control-Allow-Methods']= 'DELETE'
        return response


    if request.method == "PATCH":
        # request_url = request.headers['Origin']
        signin_user_data = json.loads(request.data)
        email = signin_user_data["email"]
        password = signin_user_data["password"]
        code, message = uesr_signin_check(email, password)
        if code == 200:
            user_name = message["user_info"][1]
            message = {"ok":True}
            response = make_response(json.dumps(message))
            response.headers['Access-Control-Allow-Origin']=request_url
            response.headers['Access-Control-Allow-Credentials']= "true"
            get_user_JWT = creat_user_JWT(user_name, email)
            response.set_cookie(key='user_token', value=get_user_JWT, expires=time.time()+6*60)
            return response
        else:
            response = make_response(json.dumps(message))
            response.headers['Access-Control-Allow-Origin']=request_url
            response.headers['Access-Control-Allow-Credentials']= "true"
            return response

    if request.method == "OPTIONS":
        message = {"ok":True}
        header_request_method = request.headers['Access-Control-Request-Method']
        # request_url = request.headers['Origin']
        response = make_response(json.dumps(message))
        response.headers['Access-Control-Allow-Origin']=request_url
        response.headers['Access-Control-Allow-Credentials']= "true"
        response.headers['Access-Control-Allow-Methods']= header_request_method
        return response
