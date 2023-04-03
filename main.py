from flask import Flask, redirect, render_template
from requests import get
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy import orm
from random import shuffle

from tools import func

from api.his import PersonalitiesResourse

from data import db_session
from data.personalities import Personalities
from data.concepts import Concepts
from data.events_dates import EventsDates

app = Flask(__name__)
api = Api(app)
db_session.global_init("db/history.db")


# con = Concepts()
# con.title = 'Тарелка'
# con.content = 'цууцйпкууцвйкпу'
# db_sess = db_session.create_session()
# db_sess.add(con)
# db_sess.commit()
@app.route("/img")
def img():
    return render_template("img.html")


@app.route("/main")
def main():
    a = get("http://127.0.0.1:8080/api/title/Путин Владимир Владимирович").json()
    res = func.get_all_info_list()
    shuffle(res)
    return render_template('test.html', res=res)


@app.route("/main/personalities")
def get_anyone():
    res = func.get_personalities_list()
    return render_template("test.html", res=res)


@app.route("/main/concepts")
def concepts():
    res = func.get_concepts_list()
    return render_template("test.html", res=res)


@app.route("/main/concepts/<string:name>")
def concept(name):
    res = func.get_concept(name)
    return render_template("test.html", res=res)


@app.route("/main/events")
def events():
    res = func.get_eventsdates_list()
    return render_template("test.html", res=res)


if __name__ == '__main__':
    api.add_resource(PersonalitiesResourse, "/api/title/<string:title>")
    app.run(host='127.0.0.1', port=8080)
