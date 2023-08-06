import logging
import os

from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Articles(base):
    __tablename__ = "articles"
    link = Column(String(100), primary_key=True)
    tittle = Column(Text)
    content = Column(Text)
    status = Column(String(100))


class MafindoNews(base):
    __tablename__ = "mafindo_tbl"
    id = Column(Integer, primary_key=True)
    authors = Column(Integer)
    status = Column(Integer)
    classification = Column(String(100))
    title = Column(Text)
    content = Column(Text)
    fact = Column(Text)
    reference_link = Column(Text)
    source_issue = Column(Text)
    source_link = Column(Text)
    picture1 = Column(String(500))
    picture2 = Column(String(100))
    tanggal = Column(String(12))
    tags = Column(String(500))
    conclusion = Column(Text)

def apply_schema(file_path: str = os.path.join(os.path.abspath(os.getcwd()), "tabayyun.db")):
    logging.info("Set SQLite as the DB engine")
    engine = create_engine("sqlite:///" + file_path)
    base.metadata.create_all(engine)

if __name__ == "__main__":
    apply_schema()
