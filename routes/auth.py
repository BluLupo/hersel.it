#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

"""
Authentication routes for login/logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
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


@route_auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not current_password or not new_password or not confirm_password:
            flash('Tutti i campi sono obbligatori.', 'danger')
            return render_template('auth/change_password.html')

        # Check current password
        if not current_user.check_password(current_password):
            flash('La password attuale non è corretta.', 'danger')
            return render_template('auth/change_password.html')

        # Check if new passwords match
        if new_password != confirm_password:
            flash('Le nuove password non corrispondono.', 'danger')
            return render_template('auth/change_password.html')

        # Check password length
        if len(new_password) < 6:
            flash('La nuova password deve essere di almeno 6 caratteri.', 'danger')
            return render_template('auth/change_password.html')

        # Update password
        current_user.set_password(new_password)
        db.session.commit()

        flash('Password modificata con successo!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('auth/change_password.html')
