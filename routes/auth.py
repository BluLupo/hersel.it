#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

"""
Authentication routes for login/logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models import User, db
from datetime import datetime

route_auth = Blueprint('auth', __name__, url_prefix='/auth')


@route_auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # Se l'utente è già autenticato, reindirizza alla dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        if not username or not password:
            flash('Per favore inserisci username e password.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Il tuo account è stato disabilitato.', 'danger')
                return render_template('auth/login.html')

            # Aggiorna last_login
            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=remember)
            flash(f'Benvenuto {user.username}!', 'success')

            # Redirect alla pagina richiesta o alla dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Username o password non corretti.', 'danger')

    return render_template('auth/login.html')


@route_auth.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    flash('Logout effettuato con successo.', 'info')
    return redirect(url_for('route_home.home'))
