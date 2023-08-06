import sqlite3 as sq
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import clear_output
import os
import random
from datetime import datetime
from . __init__ import _score_db
import markdown

__PERMISSIVE__ = True
__DBDIR__ = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".dbs")

def get_rw_feedback(a, answers):
    if answers[a][1]:
        s = '\x1b[6;30;42m' + "correct: %s"%answers[a][2] + '\x1b[0m' +"\n" #green color
        rslt = True
    else:
        s = '\x1b[5;30;41m' + "incorrect: %s"%answers[a][2] + '\x1b[0m' +"\n" #red color
        rslt = False
    return s, rslt


def record_response(qid, response, rslt):

    _sconn = sq.connect(_score_db)
    _sconn.execute("""INSERT INTO
                       scores (qid, result, response, time)
                       VALUES (?,?,?,?)""",(qid, rslt,
                                            response, datetime.now()))
    _sconn.commit()
    _sconn.close()



def assemble_ch_widget(question, answers):
    description = widgets.HTML(markdown.markdown(question))
    feedback = widgets.Output()
    check = widgets.Button(description="submit")
    options = [(a[0], i) for i, a in enumerate(answers)]

    choices = widgets.RadioButtons(
        options = options,
        description = '',
        disabled = False
    )
    return widgets.VBox([description, choices,
                         check, feedback])


def assemble_fr_widget(question):
    description = widgets.HTML(markdown.markdown(question))
    feedback = widgets.HTML()
    check = widgets.Button(description="submit")

    answer = widgets.Textarea(
                value='',
                placeholder='Type something',
                description='String:',
                disabled=False
            )
    return widgets.VBox([description, answer,
                         check, feedback])


def get_fr_widget(q, answer):

    question = q[1]
    question_tag = q[0]
    def record_answer(b):
        resp = _wdgs.children[1].value
        _wdgs.children[3].value = markdown.markdown(answer[2])
        record_response(question_tag, resp, None)


    _wdgs = assemble_fr_widget(question)
    _wdgs.children[2].on_click(record_answer)

    return _wdgs

def get_ch_widget(q, answers):

    question = q[1]
    question_tag = q[0]
    def check_selection(b):
        a = int(_wdgs.children[1].value)
        s, rslt = get_rw_feedback(a, answers)

        with _wdgs.children[3]:
            _wdgs.children[3].clear_output()
            print(s)
        record_response(question_tag, question, rslt)


    _wdgs = assemble_ch_widget(question, answers)
    _wdgs.children[2].on_click(check_selection)
    return _wdgs


def create_question_widget(mod, tag):

    conn = sq.connect(os.path.join(__DBDIR__,mod+".sqlite"))
    cursor = conn.cursor()
    cursor.execute("""SELECT
                      dmquestions.rowid,
                      dmquestions.question,
                      questiontype.type,
                      dmquestions.tags
                  FROM
                      dmquestions INNER JOIN
                          questiontype ON dmquestions.type=questiontype.rowid
                   WHERE tags = ?""",(tag,))
    q0 = cursor.fetchone()

    question_tag = q0[3]

    cursor.execute("""SELECT
                         answer, status, feedback
                      FROM
                         dmanswers
                      WHERE
                         dmanswers.qid=?""",(q0[0],))
    question_answers = cursor.fetchall()

    if q0[2] == "TF":
        w = get_ch_widget(q0, question_answers)
    elif q0[2] == "MC":
        random.shuffle(question_answers)
        w = get_ch_widget(q0, question_answers)
    elif q0[2] == "AT":
        w = get_at_widget(q0, question_answers)
    else:
        w =  get_fr_widget(q0, question_answers[0])
    conn.close()
    return w
