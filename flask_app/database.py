from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine('sqlite:///site.db',convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from flask_app import model
    Base.metadata.create_all(bind=engine)
