from data import db_session
from data.events_dates import EventsDates
from server import app
from flask_restful import abort


@app.errorhandler(404)
def abort_if_events_not_found(name, name_list):
    session = db_session.create_session()
    con = session.query(EventsDates).filter(
        EventsDates.title.like(f"%{name.title()}%") | EventsDates.title.like(
            f"%{name.lower()}%") | EventsDates.title.like(f"%{name}%")).all()
    if not con:
        if len(name_list) > 1:
            con = session.query(EventsDates).filter(
                EventsDates.title.like(f"%{name_list[0]}%") | EventsDates.title.like(
                    f"%{name_list[1] + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
            if not con:
                abort(404, message=f"Events {name} not found")
        else:
            if not con:
                abort(404, message=f"Events {name} not found")


@app.errorhandler(404)
def abort_if_event_not_found(id):
    session = db_session.create_session()
    con = session.query(EventsDates).get(id)
    if not con:
        abort(404, message=f"Event {id} not found")


@app.errorhandler(404)
def abort_if_date_not_found(dates):
    db_sess = db_session.create_session()
    date_list = db_sess.query(EventsDates).all()
    ls = []
    for i in date_list:
        date_s = i.date.split('-')
        if len(date_s) == 1:
            if int(date_s[0]) == int(dates):
                ls.append(i.to_dict(only=('title', 'title_image', 'content_image', 'id')))
        elif len(date_s) == 2:
            if int(dates) in range(int(date_s[0]), int(date_s[1])):
                ls.append(i.to_dict(only=('title', 'title_image', 'content_image', 'id')))
    if not ls:
        abort(404, message=f"Date {dates} not found")
