from skylines import app
from skylines.model import DBSession, Flight
from pprint import pformat

@app.route('/')
def index():
    q = DBSession.query(Flight)
    l = []
    for i in q:
        l.append(i.filename)

    return '<pre>' + pformat(l) + '</pre>'
