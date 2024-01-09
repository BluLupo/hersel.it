#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from sqlalchemy import Column, Integer, String, DateTime,Text, func, Boolean
from database.connection import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    author_id = Column(Integer)
    photo_article = Column(String(255))
    publish_status = Column(Boolean, nullable=False, default=False)
