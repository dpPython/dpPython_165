from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ..config import postgres_uri


engine = sqlalchemy.create_engine(postgres_uri())
Session = sessionmaker(bind=engine)


@contextmanager
def session(auto_commit=True):
    session = Session()
    try:
        yield session
        if auto_commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
