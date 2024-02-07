#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella
import bcrypt
from flask import Blueprint, render_template, request, session, url_for, redirect
from database.methods.user import get_user_by_username
from database.methods.website import get_options

route_login = Blueprint('route_login', __name__)

@route_login.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    options = get_options()[0]
    enable_login = options['enable_login']

    if enable_login == True:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            row = get_user_by_username(username)
            if username == '' or password == '':
                error = "Inserisci Username o Password Mancanti!"
                return render_template('login.html',error=error)
            if row:
                hash_and_salt = row['password'].encode('utf8')
                if bcrypt.checkpw(password.encode('utf8'), hash_and_salt):
                    session['logged_user'] = True
                    session['username'] = row['username']
                    session['userid'] = row['id']
                    return redirect(url_for('route_dashboard.dashboard'))
    else:
        return "LOGIN DISABILITATO"
    return render_template('login.html')