#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_admin = Column(Boolean, nullable=False, default=False)

    #articles = relationship('Article', back_populates='author')




