from flask_restful import Resource, reqparse
from flask import jsonify
from tools import events_dates_api_tools
from data import db_session
from data.events_dates import EventsDates
import zlib

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('content', required=True, type=str)
parser.add_argument('title_image', required=False, type=str)
parser.add_argument('content_image', required=False, type=str)
parser.add_argument('date', required=False, type=str)
parser.add_argument('century', required=False, type=str)


class EventsResourse(Resource):
    def get(self, title):
        name_list = list(item.lower().title() for item in title.split())
        events_dates_api_tools.abort_if_events_not_found(title, name_list)
        db_sess = db_session.create_session()
        cnt = db_sess.query(EventsDates).filter(EventsDates.title.like(f"%{title.title()}%") | EventsDates.title.like(
            f"%{title.lower()}%") | EventsDates.title.like(f"%{title}%")).all()
        if not cnt:
            if len(name_list) > 1:
                cnt = db_sess.query(EventsDates).filter(
                    EventsDates.title.like(f"%{name_list[0]}%") | EventsDates.title.like(
                        f"%{name_list[1] + ' ' + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
        events_dates = db_sess.query(EventsDates).get(cnt[0].id)
        res = {
            'events': events_dates.to_dict(only=('title', 'date', 'title_image', 'content_image', 'id')),
            'similar': [cnt[i].to_dict(only=('title', 'title_image', 'content_image', 'id')) for i in
                        range(1, len(cnt))] if len(cnt) > 1 else None
        }
        res["events"]["content"] = zlib.decompress(events_dates.content).decode()
        if res["similar"]:
            for item, i in zip(res["similar"], cnt[1:]):
                item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)


class EventsRes(Resource):
    def get(self, id):
        db_sess = db_session.create_session()
        events_dates_api_tools.abort_if_event_not_found(id)
        event = db_sess.query(EventsDates).get(id)
        res = {
            'event': event.to_dict(only=('title', 'date', 'title_image', 'content_image', 'id'))
        }
        res["event"]["content"] = zlib.decompress(event.content).decode()
        return jsonify(res)


class DatesResourse(Resource):
    def get(self, dates):
        db_sess = db_session.create_session()
        events_dates_api_tools.abort_if_date_not_found(dates)
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
        res = {
            'dates': ls
        }
        for item in res["dates"]:
            d = db_sess.query(EventsDates).get(item['id'])
            item["content"] = zlib.decompress(d.content).decode()
        return jsonify(res)


class EventsDatesListResourse(Resource):
    def get(self):
        db_sess = db_session.create_session()
        event_d = db_sess.query(EventsDates).all()
        res = {
            'events_dates': [item.to_dict(only=('title', 'date', 'title_image', 'content_image', 'id')) for
                             item in event_d]
        }
        for item, i in zip(res["events_dates"], event_d):
            item["content"] = zlib.decompress(i.content).decode()
        return jsonify(res)

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        event_d = EventsDates(
            title=args["title"],
            content=zlib.compress(args["content"].encode()),
            title_image=args["title_image"],
            content_image=args["content_image"],
            date=args["date"],
        )
        db_sess.add(event_d)
        db_sess.commit()
        return jsonify({'success': 'OK'})
