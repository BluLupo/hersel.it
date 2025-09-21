#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authentication Routes

from quart import Blueprint, request, render_template, redirect, url_for, session, flash
from models.user import User
from utils.auth import login_user, logout_user, get_current_user
from utils.validators import validate_email, validate_password, validate_username
from utils.helpers import flash_message

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    """Login page"""
    if request.method == 'GET':
        return await render_template('auth/login.html')
    
    form_data = await request.form
    username_or_email = form_data.get('username', '').strip()
    password = form_data.get('password', '')
    
    if not username_or_email or not password:
        flash_message('Username/Email e password sono richiesti', 'error')
        return await render_template('auth/login.html')
    
    # Authenticate user
    user = await User.authenticate(username_or_email, password)
    
    if user:
        login_user(user)
        flash_message(f'Benvenuto, {user.full_name}!', 'success')
        
        # Redirect to dashboard if admin, home otherwise
        if user.is_admin:
            return redirect(url_for('dashboard.index'))
        else:
            return redirect(url_for('home.index'))
    else:
        flash_message('Credenziali non valide', 'error')
        return await render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    """Registration page"""
    if request.method == 'GET':
        return await render_template('auth/register.html')
    
    form_data = await request.form
    username = form_data.get('username', '').strip()
    email = form_data.get('email', '').strip()
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirm_password', '')
    first_name = form_data.get('first_name', '').strip()
    last_name = form_data.get('last_name', '').strip()
    
    errors = {}
    
    # Validate inputs
    is_valid, error = validate_username(username)
    if not is_valid:
        errors['username'] = error
    
    is_valid, error = validate_email(email)
    if not is_valid:
        errors['email'] = error
    
    is_valid, error = validate_password(password)
    if not is_valid:
        errors['password'] = error
    
    if password != confirm_password:
        errors['confirm_password'] = 'Le password non coincidono'
    
    # Check if user already exists
    if not errors:
        existing_user = await User.find_by_username(username)
        if existing_user:
            errors['username'] = 'Username già in uso'
        
        existing_email = await User.find_by_email(email)
        if existing_email:
            errors['email'] = 'Email già registrata'
    
    if errors:
        for field, error in errors.items():
            flash_message(error, 'error')
        return await render_template('auth/register.html')
    
    # Create new user
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role='user'  # First user can be manually promoted to admin
    )
    user.set_password(password)
    
    try:
        await user.save()
        flash_message('Registrazione completata! Ora puoi effettuare il login.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        flash_message('Errore durante la registrazione. Riprova.', 'error')
        return await render_template('auth/register.html')

@auth_bp.route('/logout')
async def logout():
    """Logout user"""
    logout_user()
    flash_message('Logout effettuato con successo', 'success')
    return redirect(url_for('home.index'))

@auth_bp.route('/profile')
async def profile():
    """User profile page"""
    user = await get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    
    return await render_template('auth/profile.html', user=user)
