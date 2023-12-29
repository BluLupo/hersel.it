#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from database.connection import Database
from database.models.website_options import Website
from sqlalchemy.orm import close_all_sessions

db = Database()
session = db.Session()

def get_options():
    try:
        options = session.query(Website).all()
        options_list = []

        for option in options:
            opt_dict = {column.name: getattr(option, column.name) for column in Website.__table__.columns}
            options_list.append(opt_dict)

        return options_list
    finally:
        close_all_sessions()