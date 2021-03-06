from flask import *
from api.questions import app_api_questions
from api.comments import app_api_comments



app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(app_api_questions)
app.register_blueprint(app_api_comments)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
# @app.route("/attraction/<id>")
# def attraction(id):
# 	return render_template("attraction.html")
# @app.route("/booking")
# def booking():
# 	return render_template("booking.html")
# @app.route("/thankyou")
# def thankyou():
# 	return render_template("thankyou.html")

app.run(port=3000, debug=True)