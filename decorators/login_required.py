#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('route_login.login'))

    return wrap