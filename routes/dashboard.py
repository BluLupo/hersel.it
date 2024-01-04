#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, session, request
from database.methods.user import get_user_by_username
from database.methods.website import get_options,update_options
from decorators.login_required import login_required

route_dashboard = Blueprint('route_dashboard', __name__)

@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    username = session['username']
    result_username = get_user_by_username(username)
    options = get_options()[0]

    if request.method == 'POST':
        enable_register = request.form.get('enable_register')
        enable_login = request.form.get('enable_login')
        #Convert Value into Boolean Value
        enable_register = enable_register == 'on' if enable_register else False
        enable_login = enable_login == 'on' if enable_login else False
        #Update Options into Database
        update_options(enable_register=enable_register)
        update_options(enable_login=enable_login)

    return render_template('/dashboard/dashboard.html',user=result_username,options=options)