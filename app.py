from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses"

app = Flask(__name__) #review; not main
app.config['SECRET_KEY'] = "whatSecret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
num = 0 #doesn' have
responses = [] #doesn't have

@app.route('/')
def start_survey_page():

    return render_template('start_survey_page.html', survey=survey) #forgot keyword argument; have to pass survey object

@app.route('/begin') 
def ask_question(): #??need to get questions object
    """Clear the session of responses."""
    session[RESPONSES_KEY] = [] #????????
    return redirect("/questions/0") #????????

    
@app.route('/answer', methods=["POST"])
#good
def user_answer():
    answer = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses  #???
    
#need conditional here; originally had in '/question'
#my original
    # num += 1
    # if num >= 4:
    #     return render_template('/thank_you.html')
    # else:
    #     return render_template('/question.html', question = survey.questions[num])
    if (len(responses) == len(survey.questions)):
    # if len(survey.questions) >= num:
        return redirect("/complete")
        
    else:
        return redirect(f"/questions/{len(responses)}")
        
    #return redirect('/question')
@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')