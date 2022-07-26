from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import postgres_settings

engine = create_engine(postgres_settings.url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # DEPRECATED: init db structure by scripts from src/db/scripts
    # mounted to docker-entrypoint-initdb.d postgres docker container
    # Base.metadata.create_all(bind=engine)
    pass
