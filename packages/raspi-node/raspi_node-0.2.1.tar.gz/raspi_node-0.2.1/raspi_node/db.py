import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base
from .config import Config


def get_session() -> Session:
    # get the path
    path = Config.get('data_path')

    # TODO switch database strategy here
    db_name = 'backup.db'

    # build the database uri
    db_uri = f'sqlite:///{os.path.abspath(path)}/{db_name}'

    # create database if it does not exist
    if  not os.path.exists(os.path.join(path, db_name)):
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
    else:
        engine = create_engine(db_uri)
    
    # create the session
    Session = sessionmaker(bind=engine)
    return Session()
