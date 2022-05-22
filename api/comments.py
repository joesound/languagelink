from urllib import response
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, make_response
import json

from utils.comments import get_comment, create_comment

app_api_comments = Blueprint('comments', __name__, url_prefix='/api')


@app_api_comments.route("/comments", methods=['POST'])
def comments():    
    if request.method == "POST": 
        creat_comment_data = json.loads(request.data)
        if creat_comment_data["userid"] or creat_comment_data["questionid"] or creat_comment_data["content"]:
            response = make_response(json.dumps({"error":True, "message":"missing args"}))
        resp = create_comment(creat_comment_data)
        response = make_response(json.dumps(resp["message"]))
        response.headers['Access-Control-Allow-Origin']='*'
        return response


@app_api_comments.route("/comments/<id>", methods=['GET','DELETE','PATCH','OPTIONS'])
def comment_by_id(id):
    if request.method == "GET":
        resp = get_comment(id)
        response = make_response(json.dumps(resp["message"]))
        response.headers['Access-Control-Allow-Origin']='*'
        return response

    if request.method == "DELETE":
        pass

    if request.method == "PATCH": 
        pass


    if request.method == "OPTIONS": 
        pass