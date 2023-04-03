import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Concepts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "concepts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    title_image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="main-concepts.png")
    content_image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
