#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, session, redirect

route_logout = Blueprint('route_logout', __name__)

@route_logout.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session['logged_user'] = False
    return redirect('/')