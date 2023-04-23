from flask_restful import Resource, reqparse
from flask import jsonify
from tools import personalities_api_tools
from data import db_session
from data.personalities import Personalities
import zlib

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('content', required=True, type=str)
parser.add_argument('title_image', required=False, type=str)
parser.add_argument('content_image', required=False, type=str)


class PersonalitiesResourse(Resource):
    def get(self, titles):
        name_list = list(item.lower().title() for item in titles.split())
        personalities_api_tools.abort_if_personalities_not_found(titles, name_list)
        db_sess = db_session.create_session()
        cnt = db_sess.query(Personalities).filter(
            Personalities.title.like(f"%{titles.title()}%") | Personalities.title.like(
                f"%{titles.lower()}%") | Personalities.title.like(f"%{titles}%")).all()
        if not cnt:
            if len(name_list) > 1:
                cnt = db_sess.query(Personalities).filter(
                    Personalities.title.like(f"%{name_list[0]}%") | Personalities.title.like(
                        f"%{name_list[1] + ' ' + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
        personalities = db_sess.query(Personalities).get(cnt[0].id)
        res = {
            'personalities': personalities.to_dict(only=('title', 'title_image', 'content_image', 'id')),
            'similar': [cnt[i].to_dict(only=('title', 'title_image', 'content_image', 'id')) for i in
                        range(1, len(cnt))] if len(cnt) > 1 else None
        }
        res["personalities"]["content"] = zlib.decompress(personalities.content).decode()
        if res["similar"]:
            for item, i in zip(res["similar"], cnt[1:]):
                item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)


class PersonalitiesRes(Resource):
    def get(self, id):
        db_sess = db_session.create_session()
        personalities_api_tools.abort_if_personalitie_not_found(id)
        personalities = db_sess.query(Personalities).get(id)
        res = {
            'personalities': personalities.to_dict(only=('title', 'title_image', 'content_image', 'id'))
        }
        res["personalities"]["content"] = zlib.decompress(personalities.content).decode()
        return jsonify(res)


class PersonalitiesListResourse(Resource):
    def get(self):
        db_sess = db_session.create_session()
        personalities = db_sess.query(Personalities).all()
        res = {
            'personalities': [item.to_dict(only=('title', 'title_image', 'content_image', 'id')) for item in
                              personalities]
        }
        for item, i in zip(res["personalities"], personalities):
            item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        personalities = Personalities(
            title=args["title"],
            content=zlib.compress(args["content"].encode()),
            title_image=args["title_image"],
            content_image=args["content_image"]
        )
        db_sess.add(personalities)
        db_sess.commit()
        return jsonify({'success': 'OK'})
