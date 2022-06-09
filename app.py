from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)




@app.get("/")
def survey_start():
    """Returns survey start html template"""

    instructions = survey.instructions
    title = survey.title
    session['responses'] = []
    session['next_question'] = 0

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
    session['next_question'] += 1

    if session['next_question'] < len(survey.questions):
         return render_template('question.html', question_text=question, choices=choices)
    else:
        return render_template('completion.html')
   #return render_template('question.html', question_text=question, choices=choices)

@app.post("/answer")
def record_redirect():

    answer = request.form['answer']
    session['responses'] += [answer]
    next_question = session['next_question']
    
    return redirect(f'/questions/{next_question}')
