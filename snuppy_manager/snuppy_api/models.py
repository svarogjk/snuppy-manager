# coding=utf-8
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class Builds(Base):
    __tablename__ = 'builds'

    id = Column(Integer(), primary_key=True)
    unique_id = Column(String(), nullable=False, unique=True)
    app_id = Column(String(), nullable=False, unique=True)
    version = Column(String(), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    result_status = Column(Integer(), nullable=False)
    result_info = Column(String(), nullable=False)

