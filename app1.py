import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from chat import get_response
from flask_cors import CORS
from flask_session import Session
from tempfile import mkdtemp
import readfiflales

app = Flask(__name__)
CORS(app)

@app.post("/predict")
def predict():
    text =  request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

app.config["TEMPLATES_AUTO_RELOAD"] = True

questions = readfiles.readvalue("static/textfiles/questions.csv")
answers = readfiles.readlist("static/textfiles/answers.csv")
answer_key = readfiles.readvalue("static/textfiles/answerkey.csv")
media = readfiles.readmedia("static/textfiles/media.csv")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/game')
def game():
    return render_template("game.html")

@app.route('/gamestart', methods=['GET', 'POST'])
def gamestart():
    
    quiz_counter = request.values.get("quiz_counter")
    
    if quiz_counter == "0" or quiz_counter == 0:
        quiz_counter = 0
    else:
        quiz_counter = int(quiz_counter)

    if request.method == "POST":
        #determine if answer is right
        choice = request.form.get("option")
        
        if choice == answer_key[quiz_counter]:
            return render_template("correct.html", quiz_counter=str(quiz_counter), question=questions[quiz_counter], answer=answers[quiz_counter], media=media[quiz_counter], no=len(answers[quiz_counter]), key=int(answer_key[quiz_counter]))
        else: 
            return render_template("incorrect.html", quiz_counter=str(quiz_counter), question=questions[quiz_counter], answer=answers[quiz_counter], media=media[quiz_counter], no=len(answers[quiz_counter]), key=int(answer_key[quiz_counter]), choice=int(choice))
            
    else:
        if request.args.get("increment") == 1 or request.args.get("increment") == "1":
            quiz_counter = quiz_counter + 1
        #load questions
        return render_template("gamequestions.html", quiz_counter=str(quiz_counter), question=questions[quiz_counter], answer=answers[quiz_counter], media=media[quiz_counter], no=len(answers[quiz_counter]))



if __name__ == "__main__":
    app.run(debug=True)
    