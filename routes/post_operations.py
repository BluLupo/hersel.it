#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, request, redirect, url_for, session
from database.methods.user import update_username

route_changeusername = Blueprint('route_changeusername', __name__)


@route_changeusername.route('/change_username', methods=['POST'])
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        if new_username:
            try:
                print(session['userid'])
                update_username(session['userid'], new_username)
                session['username'] = new_username
            except Exception as e:
                print(f"Error updating username: {e}")
        return redirect(url_for('route_profile.profile'))
