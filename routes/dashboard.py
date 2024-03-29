#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, session, request, url_for, redirect
from database.methods.user import get_user_by_username
from database.methods.website import get_options, update_options
from decorators.login_required import login_required
from decorators.only_admin import admin
from database.methods.articles import create_article

route_dashboard = Blueprint('route_dashboard', __name__)

@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin
def dashboard():
    username = session['username']
    result_username = get_user_by_username(username)
    options = get_options()[0]

    if request.method == 'POST':
        form = request.form
        title_input = form.get('title')
        ckeditor_input = form.get('valore_editor')

        # Creare un nuovo articolo utilizzando la funzione create_article
        create_article(title=title_input, content=ckeditor_input, author_id=result_username['id'],photo_article="default.jpg")

        # Verifica da quale form proviene la richiesta
        if 'options_button_site' in form:

            enable_register = form.get('enable_register')
            enable_login = form.get('enable_login')

            # Convert Value into Boolean Value
            enable_register = enable_register == 'on' if enable_register else False
            enable_login = enable_login == 'on' if enable_login else False

            # Update Options into Database
            update_options(enable_register=enable_register)
            update_options(enable_login=enable_login)

        return redirect(url_for('route_dashboard.dashboard'))

    return render_template('/dashboard/dashboard.html', user=result_username, options=options)

