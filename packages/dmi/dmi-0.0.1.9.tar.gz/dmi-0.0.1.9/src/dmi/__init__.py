import os
import sqlite3 as sq
from .version import __version__


_score_dir = os.path.join(os.path.expanduser("~"), ".dminteract")
if not os.path.exists(_score_dir):
    os.mkdir(_score_dir)

_score_db = os.path.join(_score_dir, "scores.sqlite")

if not os.path.exists(_score_db):
    _sconn = sq.connect(_score_db)
    _sc = _sconn.cursor()
    _sc.execute("""CREATE TABLE IF NOT EXISTS
                       scores (qid INT,
                               result BOOL,
                               response TEXT,
                               time DATE)""")
    _sconn.commit()
    _sconn.close()
