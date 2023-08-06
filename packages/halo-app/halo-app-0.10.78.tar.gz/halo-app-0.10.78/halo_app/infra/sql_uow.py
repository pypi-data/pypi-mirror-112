# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from halo_app.app.uow import AbsUnitOfWork, AbsUnitOfWorkManager
from halo_app.infra.exceptions import UnitOfWorkConfigException
from halo_app.infra.sql_repository import SqlAlchemyRepository
from halo_app.settingsx import settingsx

settings = settingsx()


class SqlAlchemyUnitOfWorkManager(AbsUnitOfWorkManager):

    def __init__(self, session_factory=None):
        if session_factory:
            self.session_factory = session_factory
        else:
            DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
                settings.SQLALCHEMY_DATABASE_URI,
                isolation_level=settings.ISOLATION_LEVEL
            ))
            self.session_factory = DEFAULT_SESSION_FACTORY

    def start(self,method_id=None) -> AbsUnitOfWork:
        #if method_id in list:
        return SqlAlchemyUnitOfWork(self.session_factory())

class SqlAlchemyUnitOfWork(AbsUnitOfWork):

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self.repository = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


