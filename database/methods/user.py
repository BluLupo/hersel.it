#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from database.connection import Database
from database.models.user import User

db = Database()
session = db.Session()

def create_user(username, email, password):
    try:
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
    finally:
        session.close()

def get_users():
    users = session.query(User).all()
    user_list = []

    for user in users:
        user_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns}
        user_list.append(user_dict)

    return user_list

def get_user_by_id(user_id):
    user = session.query(User).filter_by(id=user_id).first()

    if user:
        user_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns}
        return user_dict
    else:
        return None  # Utente non trovato

def get_user_by_username(username):
    user = session.query(User).filter_by(username=username).first()

    if user:
        user_dict = {column.name: getattr(user, column.name) for column in User.__table__.columns}
        return user_dict
    else:
        return None  # Utente non trovato


