#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

import bcrypt
from flask import Blueprint, render_template, request
from database.methods.user import create_user
from database.methods.website import get_options

route_register = Blueprint('route_register', __name__)

@route_register.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    options = get_options()[0]
    enable_reg = options['enable_register']

    if enable_reg == True:
        if request.method == 'POST':
            form = request.form
            email = form['email']
            username = form['username']
            password = form['password']

            if email == '' or username == '' or password == '':
                error = "Ci sono dei dati mancanti!"
                return render_template('register.html', error=error)

            # Hash della password con salt
            hash_and_salt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Converti l'hash in esadecimale
            hex_hash = hash_and_salt.decode('utf-8')

            create_user(username, email, hex_hash)
    else:
        return "REGISTRAZIONE DISABILITATA"

    return render_template('register.html')
