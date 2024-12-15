from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker #, Session
import models as m

main_engine = sa.create_engine(
    "postgresql://user:password@postgres:5432/dating_database",
    echo=True,
)

DBSession = sessionmaker(
    binds={
        m.Base: main_engine,
    },
    expire_on_commit=False,
)

@contextmanager
def session_scope(): #-> Session:
    """Provides a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()



def get_db_session(session: Session = Depends(session_scope)) -> Session:
    """Зависимость для получения сессии через session_scope"""
    return session