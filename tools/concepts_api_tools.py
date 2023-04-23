from data import db_session
from data.concepts import Concepts
from flask_restful import abort
from server import app


@app.errorhandler(404)
def abort_if_concepts_not_found(name, name_list):
    session = db_session.create_session()
    con = session.query(Concepts).filter(Concepts.title.like(f"%{name.title()}%") | Concepts.title.like(
        f"%{name.lower()}%") | Concepts.title.like(f"%{name}%")).all()
    if not con:
        if len(name_list) > 1:
            con = session.query(Concepts).filter(
                Concepts.title.like(f"%{name_list[0]}%") | Concepts.title.like(
                    f"%{name_list[1] + name_list[2] if len(name_list) >= 3 else name_list[1]}%")).all()
            if not con:
                abort(404, message=f"Concepts {name} not found")
        else:
            abort(404, message=f"Concepts {name} not found")


@app.errorhandler(404)
def abort_if_concept_not_found(id):
    session = db_session.create_session()
    con = session.query(Concepts).get(id)
    if not con:
        abort(404, message=f"Concepts {id} not found")
