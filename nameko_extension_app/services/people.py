from nameko import rpc

import nameko_redis
import nameko_logstash

from ..utils import cache as _cache
from ..utils import log as _log
from ..utils.db import models as _models
from ..utils.db import orm as _orm
from ..utils.db import session as _session


class PeopleService(object):
    # service name
    name = 'people'

    # redis cache related
    people_key = 'people'
    redis = nameko_redis.Redis('development')

    # db session
    session = _session.DbSession(_models.DeclarativeBase)

    # logging
    log = nameko_logstash.LogstashDependency(local_file='./_persistent/logs/people_service.log')

    @rpc.rpc
    def ping(self):
        return 'pong!'

    @rpc.rpc
    def get_people(self):
        """ get the listed people from system
        """

        # try to get the people from cache.
        try:
            people = _cache.get_people(self.redis, self.people_key)
            _log.get_people(self.log, 'info', self.people_key, people, 'cache')
            return people

        except Exception as e:
            _log.log(self.log, 'warn', str(e).encode())

            # try from db
            try:
                people = _orm.get_all_people(self.session, _models.Person)
                _log.get_people(self.log, 'info', self.people_key, people, 'db')

                # cache missing these entries, add them to cache
                try:
                    _cache.add_people(self.redis, self.people_key, people)
                except Exception as e:
                    _log.log(self.log, 'warn', str(e).encode())

                # get values from cache
                return _cache.get_people(self.redis, self.people_key)

            except Exception as e:
                _log.log(self.log, 'error', str(e).encode())

    @rpc.rpc
    def add_person(self, name, age):
        """ Add person to system
        """
        try:
            age = int(age)
        except Exception as e:
            _log.log(self.log, 'error', str(e).encode())
            return False

        person = _models.Person(name=name, age=age)

        # person key exists in cache, return false
        if _cache.person_exists(self.redis, self.people_key, person):
            return False

        # person key exists in db, add it to cache and return false
        if _orm.person_exists(self.session, _models.Person, _models.Person.name, name):
            try:
                _cache.add_people(self.redis, self.people_key, [person])
            except Exception as e:
                _log.log(self.log, 'warn', str(e).encode())
            
            return False

        # add person to db
        try:
            _orm.add_people(self.session, [person])
            _log.add_person(self.log, 'info', self.people_key, person, 'db')
        except Exception as e:
            _log.log(self.log, 'error', str(e).encode())
            return False

        # add person to cache
        try:
            _cache.add_people(self.redis, self.people_key, [person])
            _log.add_person(self.log, 'info', self.people_key, person, 'cache')
        except Exception as e:
            _log.log(self.log, 'warn', str(e).encode())

        return True
    
    @rpc.rpc
    def clear_cache(self):
        _log.log(self.log, 'info', 'Clear cache.')
        return _cache.clear(self.redis)
