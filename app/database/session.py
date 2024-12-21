import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from . import models as m

# Создание движка базы данных
main_engine = sa.create_engine(
    "postgresql://user:password@postgres:5432/dating_database",
    echo=True,
)

# Настройка Session
DBSession = sessionmaker(
    binds={},
    bind=main_engine,  # Используем bind здесь
    expire_on_commit=False,
)

@contextmanager
def session_scope():
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

def get_db_session() -> Session:
    """Зависимость для получения сессии через session_scope."""
    with session_scope() as session:
        yield session