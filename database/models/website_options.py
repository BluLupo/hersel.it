#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from sqlalchemy import Column, Integer, Boolean
from database.connection import Base

class Website(Base):
    __tablename__ = 'website_options'
    id = Column(Integer, primary_key=True, autoincrement=True)
    enable_register = Column(Boolean, nullable=False, default=False)
    enable_login = Column(Boolean, nullable=False, default=False)

