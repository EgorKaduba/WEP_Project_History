from flask_restful import Resource, reqparse
from flask import jsonify
from tools import concepts_api_tools
from data import db_session
from data.concepts import Concepts
import zlib

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('content', required=True, type=str)
parser.add_argument('title_image', required=False, type=str)
parser.add_argument('content_image', required=False, type=str)


class ConceptsRes(Resource):
    def get(self, id):
        db_sess = db_session.create_session()
        concepts_api_tools.abort_if_concept_not_found(id)
        concepts = db_sess.query(Concepts).get(id)
        res = {
            "concepts": concepts.to_dict(only=('title', 'title_image', 'content_image', 'id'))
        }
        res["concepts"]["content"] = zlib.decompress(concepts.content).decode()
        return jsonify(res)


class ConceptsListResourse(Resource):
    def get(self):
        db_sess = db_session.create_session()
        concepts = db_sess.query(Concepts).all()
        res = {
            "concepts": [item.to_dict(only=('title', 'title_image', 'content_image', 'id')) for item in concepts]
        }
        for item, i in zip(res["concepts"], concepts):
            item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        concept = Concepts(
            title=args["title"],
            content=zlib.compress(args["content"].encode()),
            title_image=args["title_image"],
            content_image=args["content_image"]
        )
        db_sess.add(concept)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ConceptsResourse(Resource):
    def get(self, titles):
        name_list = list(item.lower().title() for item in titles.split())
        concepts_api_tools.abort_if_concepts_not_found(titles, name_list)
        db_sess = db_session.create_session()
        cnt = db_sess.query(Concepts).filter(Concepts.title.like(f"%{titles.title()}%") | Concepts.title.like(
            f"%{titles.lower()}%") | Concepts.title.like(f"%{titles}%")).all()
        if not cnt:
            if len(name_list) > 1:
                cnt = db_sess.query(Concepts).filter(Concepts.title.like(f"%{name_list[0]}%") | Concepts.title.like(
                    f"%{name_list[1] + ' ' + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
        concepts = db_sess.query(Concepts).get(cnt[0].id)
        res = {
            'concepts': concepts.to_dict(only=('title', 'title_image', 'content_image', 'id')),
            'similar': [cnt[i].to_dict(only=('title', 'title_image', 'content_image', 'id')) for i in
                        range(1, len(cnt))] if len(cnt) > 1 else None
        }
        res["concepts"]["content"] = zlib.decompress(concepts.content).decode()
        if res["similar"]:
            for item, i in zip(res["similar"], cnt[1:]):
                item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)
