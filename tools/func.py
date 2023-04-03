from sqlalchemy import func
from data import db_session
from data.personalities import Personalities
from data.concepts import Concepts
from data.events_dates import EventsDates
from main import app
from flask_restful import reqparse, abort, Api, Resource


@app.errorhandler(404)
def abort_if_personalities_not_found(title):
    session = db_session.create_session()
    titles = session.query(Personalities).get(1)
    a = session.query(Personalities).filter(Personalities.title == f"{title}").all()
    if not title:
        abort(404, message=f"Personalities {title} not found")


def get_all_info_list():
    db_sess = db_session.create_session()
    con = db_sess.query(Concepts).all()
    per = db_sess.query(Personalities).all()
    dat = db_sess.query(EventsDates).all()
    res1 = [[item.title, item.content, item.title_image] for item in con]
    res2 = [[item.title, item.content, item.title_image] for item in per]
    res3 = [[item.title, item.content, item.title_image] for item in dat]
    res = res1 + res2 + res3
    return res


def get_personalities_list():
    db_sess = db_session.create_session()
    pers = db_sess.query(Personalities).all()
    res = [[item.title, item.content, item.title_image] for item in pers]
    return res


def get_concepts_list():
    db_sess = db_session.create_session()
    cons = db_sess.query(Concepts).all()
    res = [[item.title, item.content, item.title_image] for item in cons]
    return res


def get_eventsdates_list():
    db_sess = db_session.create_session()
    dat = db_sess.query(EventsDates).all()
    res = [[item.title, item.content, item.title_image] for item in dat]
    return res


def get_concept(name):
    db_sess = db_session.create_session()
    name_list = [name.title(), name.lower(),
                 name.split()[0].title() + name.split()[1].lower() if len(name.split()) == 2 else '']
    con = db_sess.query(Concepts).filter(
        Concepts.title.like(f"%{name_list[0]}%") | Concepts.title.like(f"%{name_list[1]}%") | Concepts.title.like(
            f"%{name_list[2]}%"))
    res = [[item.title, item.content, item.title_image] for item in con]
    return res
