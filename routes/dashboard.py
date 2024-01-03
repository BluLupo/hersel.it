#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, session, request
from database.methods.user import get_user_by_username
from database.methods.website import get_options
from decorators.login_required import login_required

route_dashboard = Blueprint('route_dashboard', __name__)

@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    username = session['username']
    result_username = get_user_by_username(username)
    options = get_options()[0]
    print(options['enable_login'])
    print(result_username)
    if request.method == 'POST':
        print("POST")
    return render_template('/dashboard/dashboard.html',user=result_username)