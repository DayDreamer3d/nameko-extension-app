import sqlalchemy
from sqlalchemy.ext import declarative


class Base(object):
    pass


DeclarativeBase = declarative.declarative_base(cls=Base)


class Person(DeclarativeBase):
    __tablename__ = 'people'

    id_ = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100))
    age = sqlalchemy.Column(sqlalchemy.Integer)
