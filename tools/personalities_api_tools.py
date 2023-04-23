from data import db_session
from data.personalities import Personalities

from server import app

from flask_restful import abort


@app.errorhandler(404)
def abort_if_personalities_not_found(name, name_list):
    session = db_session.create_session()
    con = session.query(Personalities).filter(Personalities.title.like(f"%{name.title()}%")).all()
    if not con:
        if len(name_list) > 1:
            con = session.query(Personalities).filter(
                Personalities.title.like(f"%{name_list[0]}%") | Personalities.title.like(
                    f"%{name_list[1] + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
            if not con:
                abort(404, message=f"Personalities {name} not found")
        else:
            abort(404, message=f"Personalities {name} not found")


@app.errorhandler(404)
def abort_if_personalitie_not_found(id):
    session = db_session.create_session()
    con = session.query(Personalities).get(id)
    if not con:
        abort(404, message=f"Personalities {id} not found")
