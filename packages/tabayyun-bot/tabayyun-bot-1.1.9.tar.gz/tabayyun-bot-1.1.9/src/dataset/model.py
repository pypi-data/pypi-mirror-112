import logging
import os

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


class Articles(base):
    __tablename__ = "articles"
    link = Column(String(100), primary_key=True)
    tittle = Column(Text)
    content = Column(Text)
    status = Column(String(100))


def apply_schema(file_path: str = os.path.join(os.path.abspath(os.getcwd()), "tabayyun.db")):
    logging.info("Set SQLite as the DB engine")
    engine = create_engine("sqlite:///" + file_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    base.metadata.create_all(engine)


if __name__ == "__main__":
    apply_schema()
