#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from database.connection import Database
from database.models.website_options import Website
from sqlalchemy.orm import close_all_sessions

db = Database()
session = db.Session()

def create_data_website_options():
    existing_website = session.query(Website).filter_by(id=1).first()

    if existing_website:
        print("La riga con ID 1 esiste già nel database. Non è necessario aggiornarla.")
    else:
        initial_data = {'enable_login': False, 'enable_register': False}
        initial_website = Website(id=1, **initial_data)
        session.add(initial_website)
        session.commit()
        print("Riga con ID 1 creata nel database.")


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



def update_options(enable_login=None, enable_register=None):
    # Trova il sito da aggiornare
    website = session.query(Website).filter_by(id=1).first()

    if website:
        # Aggiorna i campi con i nuovi valori, se specificati
        if enable_login is not None:
            website.enable_login = enable_login
        if enable_register is not None:
            website.enable_register = enable_register

        # Esegui il commit per applicare l'aggiornamento nel database
        session.commit()
        print("Opzioni del sito aggiornate correttamente.")
    else:
        print("Sito non trovato.")
