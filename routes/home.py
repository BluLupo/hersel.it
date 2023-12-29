#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template
from utilities.aboutclass import BluLupo
from database.methods.user import create_user,get_users, get_user_by_id, get_user_by_username

route_home = Blueprint('route_home', __name__)

@route_home.route('/', methods=['GET', 'POST'])
def home():
    me = BluLupo()
    result = get_users()

    # Stampa i dettagli di tutti gli utenti
    for user_details in result:
        print(user_details['username'])

    user_id_to_get = 1  # Sostituisci con l'ID desiderato
    single_result = get_user_by_id(user_id_to_get)
    single_result_username = get_user_by_username('hersel')
    print(single_result)
    print(single_result_username)


    return render_template('home.html',user=result,me=me)