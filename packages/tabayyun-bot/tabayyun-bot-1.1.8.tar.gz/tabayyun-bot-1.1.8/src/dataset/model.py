import logging
import os

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.info("Set SQLite as the DB engine")
file_path = os.path.join(os.path.abspath(os.getcwd()), "tabayyun.db")
engine = create_engine("sqlite:///" + file_path)

base = declarative_base()


class DmpLog(base):
    __tablename__ = "articles"
    link = Column(String(100), primary_key=True)
    tittle = Column(Text)
    content = Column(Text)
    status = Column(String(100))

Session = sessionmaker(bind=engine)
session = Session()
base.metadata.create_all(engine)
