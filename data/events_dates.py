import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class EventsDates(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "events_dates"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    century = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    title_image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="main-date.png")
    content_image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
