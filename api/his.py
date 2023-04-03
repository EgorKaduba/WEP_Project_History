from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from tools import func
from data import db_session
from data.personalities import Personalities


class PersonalitiesResourse(Resource):
    def get(self, title):
        func.abort_if_personalities_not_found(title)
        db_sess = db_session.create_session()
        personalities = db_sess.query(Personalities).get(1)
        return jsonify({'personalities': personalities.to_dict(only=('title', 'content'))})
