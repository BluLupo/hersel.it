#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from functools import wraps
from flask import redirect, url_for, session, render_template
from database.methods.user import get_user_by_username

def admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = session['username']
        user = get_user_by_username(username)
        if user['is_admin'] == True:
            return f(*args, **kwargs)
        else:
            msg = "Non sei un amministratore non puoi visualizzare questa pagina!"
            #return redirect(url_for('route_home.home'))
            return render_template('error.html', message=msg)

    return wrap