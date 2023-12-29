#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

DATABASE_URL = 'mysql+pymysql://{username}:{password}@{host}/{db}'.format(
    username=Config.USER,
    password=Config.PASSWORD,
    host=Config.HOST,
    db=Config.DB
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base(metadata=MetaData())

class Database:
    def __init__(self):
        self.engine = engine
        self.Session = Session

    def create_tables(self):
        # Crea tutte le tabelle
        Base.metadata.create_all(bind=self.engine)
