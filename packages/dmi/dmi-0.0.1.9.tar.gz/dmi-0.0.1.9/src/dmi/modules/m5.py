import os
from .. import eval as _e


def get_tags(mod):
    import sqlite3 as sq
    conn = sq.connect(os.path.join(_e.__DBDIR__,mod+".sqlite"))
    c = conn.cursor()
    c.execute("""SELECT tags FROM dmquestions""")
    tags = [t[0] for t in c.fetchall()]
    return tags

_tags = get_tags("m5")
_m5_groups = ['qbank1', 'qbank2', 'qbank3']
_m5_evals = {key:[t for t in _tags if key in t] for key in _m5_groups}

__scores = {key:{} for key in _m5_evals.keys()}

del _tags

question_banks = {key:{tag:_e.create_question_widget("m5", tag) for tag in _m5_evals[key]}
                     for key in _m5_evals.keys() }
