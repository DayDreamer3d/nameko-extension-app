import sqlite
import sqlachemy
from sqlachemy.ext.declarative

from nameko import rpc
import nameko_sqlalchemy


Base = declarative.declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id_ = sqlachemy.Column(sqlachemy.Integer, primary_key=True)
    name = sqlachemy.Column(sqlachemy.String)
    age = sqlachemy.Column(sqlachemy.Integer)


engine = sqlachemy.create_engine('sqlite://')
Base.metadata.create_all(engine)


class OrmService(object):
    name = 'orm'
    session = nameko_sqlalchemy.Session(Base)

    @rpc.rpc
    def get_listed_people(self, name):
        person = self.session.query(Person).get(name=name)
        return person.name, person.age

    @rpc.rpc
    def add_person(self, name, age):
        age = int(age)
        person = Person(name=name, age=age)
        self.session.add(person)
        self.session.commit()
