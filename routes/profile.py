#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, make_response, session
from database.methods.user import get_user_by_username
from decorators.login_required import login_required

route_profile = Blueprint('route_profile', __name__)
@route_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = session['username']
    result_username = get_user_by_username(username)

    if result_username['id'] == session['userid']:
        response = make_response(render_template('profile.html',user=result_username))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    else:
        return "Non sei autorizzato a visualizzare questo elemento!"

    return response