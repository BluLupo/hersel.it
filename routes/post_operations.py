#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, request, redirect, url_for, session, render_template
from database.methods.user import update_username
from decorators.login_required import login_required
from database.methods.user import get_user_by_username

route_changeusername = Blueprint('route_changeusername', __name__)
route_changepassword = Blueprint('route_changepassword', __name__)


@route_changeusername.route('/change_username', methods=['POST'])
@login_required
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        if new_username:
            try:
                update_username(session['userid'], new_username)
                session['username'] = new_username
            except Exception as e:
                print(f"Error updating username: {e}")
        return redirect(url_for('route_profile.profile'))

@route_changepassword.route('/change_password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        username = session['username']
        result_username = get_user_by_username(username)
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        if current_password == new_password:
            #update_password(session['userid'], new_password)
            print(current_password)
            print(new_password)
        else:
            error_message = "Le password non coincidono!"
            return render_template('profile.html', error_message=error_message,user=result_username)

        return redirect(url_for('route_profile.profile'))

