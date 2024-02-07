#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, make_response, session
from database.methods.user import get_user_by_username

route_profile = Blueprint('route_profile', __name__)
@route_profile.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session['username']
    result_username = get_user_by_username(username)
    print(result_username)
    response = make_response(render_template('profile.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response