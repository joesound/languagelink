from urllib import response
from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, make_response
import json

from utils.question import create_question, get_question, delete_question, update_question

app_api_questions = Blueprint('questions', __name__, url_prefix='/api')

@app_api_questions.route("/questions", methods=['GET','POST'])
def questios():
    if request.method == "GET":
        get_query_page = request.args.get('page')
        resp = get_question(get_query_page)
        response = make_response(json.dumps(resp["message"]))
        response.headers['Access-Control-Allow-Origin']='*'
        return response
        
    if request.method == "POST": 
        creat_question_data = json.loads(request.data)
        if creat_question_data["userid"] or creat_question_data["title"] or creat_question_data["content"]:
            response = make_response(json.dumps({"error":True, "message":"missing args"}))
        resp = create_question(creat_question_data)
        response = make_response(json.dumps(resp["message"]))
        response.headers['Access-Control-Allow-Origin']='*'
        return response



@app_api_questions.route("/questions/<id>", methods=['DELETE','PATCH','OPTIONS'])
def question_by_id(id):
    if request.method == "DELETE":
        pass

    if request.method == "PATCH": 
        pass


    if request.method == "OPTIONS": 
        pass

