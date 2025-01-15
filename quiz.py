# Тут буде код веб-програми
from flask import Flask, session, redirect, url_for, request, render_template
from random import randint
from db_scripts import get_question_after, get_quises, check_answer
import os
from random import shuffle
def start_quiz (quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()
    
def quiz_form():
    # html_beg = '''<html><body><h2>Select quiz</h2>
    # <form method="post" action="index">
    # <select name="quiz">
    # '''
    # html_end = '''
    # </select>
    # <input type="submit" value="Вибрати">
    # </form>
    # </body></html>'''
    # options = ''''''
    # quiz_list = get_quises()
    # for id, name in quiz_list:
    #     options += f'<option value="{str(id)}">{str(name)}</option>'
    # return html_beg + options + html_end
    q_list = get_quises()
    return render_template('start.html', q_list = q_list)

def index():
    # global quiz, last_question
    # max_quiz = 3
    # session['quiz'] = randint(1, max_quiz)
    # session['last_question'] = 0
    # return '<a href="/test">TEST</a>'
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(int(quiz_id))
        return redirect(url_for('test'))
    
    
def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1
        
def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html', question = question[1], quest_id = question[0], answers_list = answers_list)

def test():
    # global last_question
    if not ('quiz' in session) or int(session['quiz']) < 0 :
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            save_answers()
        question = get_question_after(session['last_question'], session['quiz'])
        if question is None or len(question) == 0:
            return redirect(url_for('result'))
        else:
            # session['last_question'] = question[0]
            # return f"Quiz {session['quiz']}: <h1>{question[1]}</h1><br>{question[2]}<br>{question[3]}<br>{question[4]}<br>{question[5]}"
            return question_form(question)
def result():
    html = render_template('result.html', right = session['answers'], total = session["total"])
    end_quiz()
    return html


folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.add_url_rule("/", "index", index, methods=['GET', 'POST'])
app.add_url_rule("/index", "index", index, methods=['GET', 'POST'])
app.add_url_rule("/test", "test", test, methods=['GET', 'POST'])
app.add_url_rule("/result", "result", result)
app.config['SECRET_KEY'] = "Abbabahalamaha"
if __name__ == '__main__':
    app.run()