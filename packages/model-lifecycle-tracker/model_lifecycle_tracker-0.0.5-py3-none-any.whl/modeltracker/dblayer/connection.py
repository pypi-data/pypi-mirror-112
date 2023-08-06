import sys
import modeltracker.settings_local as settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
import logging.config
log = logging.getLogger(__name__)


def connection_string(engine, host, port, username, password, database):
    return '{engine}{username}:{password}@{host}:{port}/{database}'.format(
        engine=engine,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database)


class DbSession(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if DbSession.__instance is None:
            DbSession.__instance = object.__new__(cls)
            try:
                cls.engine = create_engine(connection_string(
                    engine=kwargs['engine'],
                    host=kwargs['host'],
                    port=kwargs['port'],
                    username=kwargs['username'],
                    password=kwargs['password'],
                    database=kwargs['database']
                ), echo=settings.DEBUG)
                log.debug('activating session')
                cls.session = sessionmaker(bind=cls.engine, autocommit=False, autoflush=True)()
            except KeyError as e:
                print('DbSession available')
        return DbSession.__instance

    def __init__(self, **kwargs):
        """
        :param username: a database username
        :param password: database password
        :param host: ip of host
        :param port: port of db
        :param database: a database name
        """
        pass



