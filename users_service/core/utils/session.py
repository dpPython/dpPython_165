from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from config import Config

engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


@contextmanager
def session(auto_commit=True):
    session = Session()
    try:
        yield session
        if auto_commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
