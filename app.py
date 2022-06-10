from http.client import responses
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

    return render_template("survey_start.html",
        title=survey.title,instructions=survey.instructions)

@app.post('/begin')
def send_to_question():
    """ Redirects to the url to show the first question """
    session['responses'] = []
    return redirect(f"/questions/0")

@app.get('/questions/<int:question_num>')
def show_questions(question_num):
    """ Displays the question based on the index input into the url if survey is complete
    shows completion.html or redirects to right question if user skips question"""
    if not int(question_num) == len(session['responses']):
        correct_question_num = len(session['responses'])
        flash('Accessing invalid question.')
        return redirect(f'/questions/{correct_question_num}')

    if int(question_num) < len(survey.questions):
        question = survey.questions[int(question_num)].question
        choices = survey.questions[int(question_num)].choices
        return render_template('question.html', question_text=question, choices=choices,question_num=question_num+1)

    else:
        return render_template('completion.html')

@app.post("/answer")
def record_redirect():
    """ Updates the session's responses list with the user's input.
        Then redirects the user to the next question's url.
    """
    answer = request.form['answer']
    session['responses'] += [answer]
    question_num = len(session['responses'])

    return redirect(f'/questions/{question_num}')
