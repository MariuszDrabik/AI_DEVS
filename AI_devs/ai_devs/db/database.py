from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import settings


POSTGRES_URL = (
    f"""postgresql://{settings.POSTGRES_USER}:"""
    f"""{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:"""
    f"""{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"""
)


engine = create_engine(POSTGRES_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        # Handle exceptions if needed
        db.rollback()
        raise e
    finally:
        db.close()
