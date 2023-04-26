from data import db_session
from data.personalities import Personalities
from data.concepts import Concepts
from data.events_dates import EventsDates
import zlib
import requests


def get_all_info_list():
    db_sess = db_session.create_session()
    con = db_sess.query(Concepts).all()
    per = db_sess.query(Personalities).all()
    dat = db_sess.query(EventsDates).all()
    res1 = [[item.title, zlib.decompress(item.content).decode(), item.title_image, item.id, 'concepts'] for item in con]
    res2 = [[item.title, zlib.decompress(item.content).decode(), item.title_image, item.id, 'personalities'] for item in
            per]
    res3 = [[item.title, zlib.decompress(item.content).decode(), item.title_image, item.id, 'events_dates'] for item in
            dat]
    res = res1 + res2 + res3
    return res


def get_group_list(group):
    db_sess = db_session.create_session()
    ls = ''
    if group == "concepts":
        ls = db_sess.query(Concepts).all()
    elif group == "personalities":
        ls = db_sess.query(Personalities).all()
    elif group == "events_dates":
        ls = db_sess.query(EventsDates).all()
    res = [[item.title, zlib.decompress(item.content).decode(), item.title_image, item.id, group] for item in ls]
    return res


def get_for_id(group, id):
    db_sess = db_session.create_session()
    res = []
    if group == "concepts":
        res = db_sess.query(Concepts).get(id)
    elif group == "personalities":
        res = db_sess.query(Personalities).get(id)
    elif group == "events_dates":
        res = db_sess.query(EventsDates).get(id)
    new_content = zlib.decompress(res.content).decode().split(' | ')
    return [res.title, new_content, res.title_image, res.content_image.split(" | ") if res.content_image else None,
            res.date if group == "events_dates" else None]


def search_all(searh_text):
    res = []
    con = []
    dat = []
    per = []
    event = []
    while not res:
        ss = list()
        a = list(i in '1234567890' for i in searh_text)
        if all(a):
            dat = requests.get(f"https://e3f7-46-236-191-178.ngrok-free.app/api/dates/date/{searh_text}").json()
            ss.append(dat)
        a = list(i not in '1234567890' for i in searh_text)
        if all(a):
            con = requests.get(f"https://e3f7-46-236-191-178.ngrok-free.app/api/concepts/title/{searh_text}").json()
            per = requests.get(f"https://e3f7-46-236-191-178.ngrok-free.app/api/personalities/title/{searh_text}").json()
            event = requests.get(f"https://e3f7-46-236-191-178.ngrok-free.app/api/events/title/{searh_text}").json()
            ss = [con, per, event]
        for t in ss:
            if t == con:
                k = 'concepts'
                b = 'concepts'
            elif t == per:
                k = 'personalities'
                b = 'personalities'
            elif t == event:
                k = 'events'
                b = 'events_dates'
            else:
                k = 'dates'
                b = 'events_dates'
            if 'message' not in t.keys():
                if type(t[k]) == list:
                    for j in t[k]:
                        ls = [j['title'], j['content'], j['title_image'], j['id'], b]
                        res.append(ls)
                else:
                    ls = [t[k]['title'], t[k]['content'], t[k]['title_image'], t[k]['id'], b]
                    res.append(ls)
                if 'similar' in t.keys():
                    if t['similar']:
                        for i in t['similar']:
                            ls = [i['title'], i['content'], i['title_image'], i['id'], b]
                            res.append(ls)
        if len(searh_text) != 1 or not res:
            if res:
                return res
            if len(searh_text) != 1:
                searh_text = searh_text[:len(searh_text) - 1]
            else:
                return None
    return res


def search_group(group, searh_text):
    res = []
    con = ''
    k = ''
    if group == 'concepts':
        con = requests.get(f"http://127.0.0.1:8080/api/concepts/title/{searh_text}").json()
        k = 'concepts'
    elif group == 'personalities':
        con = requests.get(f"http://127.0.0.1:8080/api/personalities/title/{searh_text}").json()
        k = 'personalities'
    elif group == 'events_dates':
        if all(list(i in '1234567890' for i in searh_text)):
            con = requests.get(f"http://127.0.0.1:8080/api/dates/date/{searh_text}").json()
            k = 'dates'
        elif all(list(i not in '1234567890' for i in searh_text)):
            con = requests.get(f"http://127.0.0.1:8080/api/events/title/{searh_text}").json()
            k = 'events'
    while not res:
        if 'message' not in con.keys():
            if type(con[k]) == list:
                for j in con[k]:
                    ls = [j['title'], j['content'], j['title_image'], j['id'], group]
                    res.append(ls)
            else:
                ls = [con[k]['title'], con[k]['content'], con[k]['title_image'],
                      con[k]['id'], group]
                res.append(ls)
            if 'similar' in con.keys():
                if con['similar']:
                    for i in con['similar']:
                        ls = [i['title'], i['content'], i['title_image'], i['id'], group]
                        res.append(ls)
        if len(searh_text) != 1 or not res:
            if res:
                return res
            if len(searh_text) != 1:
                searh_text = searh_text[:len(searh_text) - 1]
            else:
                return None
    return res
