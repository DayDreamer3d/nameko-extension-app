import nameko_sqlalchemy


class DbSession(nameko_sqlalchemy.Session):
    def setup(self):
        super(DbSession, self).setup()
        self.declarative_base.metadata.create_all(self.engine)
