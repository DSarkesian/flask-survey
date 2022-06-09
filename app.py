from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responces = []

@app.get("/")
def survey_start():
    """Returns survey start html template"""

    instructions = survey.instructions
    title = survey.title

    return render_template("survey_start.html",
        title=title,instructions=instructions)

@app.post('/begin')
def send_to_question():
    """ Redirects to the url to show the first question """

    return redirect(f"/questions/0")

@app.get('/questions/<question_nmbr>')
def show_questions(question_nmbr):
    """ Displays the question based on the index input into the url"""
    question = survey.questions[int(question_nmbr)].question
    choices = survey.questions[int(question_nmbr)].choices
    
    return render_template('question.html', question_text=question, choices=choices)
    # if int(question) < len(survey.questions) - 1:
    #     return redirect(f'/question/{int(question) + 1}', 
    #     question.question= survey.questions[int(question) + 1].question)
