#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authentication Utilities

from functools import wraps
from quart import session, request, redirect, url_for, jsonify
from typing import Optional
from models.user import User

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('auth.login'))
        return await f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('auth.login'))
        
        user = await get_current_user()
        if not user or not user.is_admin:
            if request.is_json:
                return jsonify({'error': 'Admin access required'}), 403
            return redirect(url_for('home.index'))
        
        return await f(*args, **kwargs)
    return decorated_function

async def get_current_user() -> Optional[User]:
    """Get the currently logged-in user"""
    if 'user_id' not in session:
        return None
    
    try:
        user_id = session['user_id']
        return await User.find_by_id(user_id)
    except:
        # Clear invalid session
        session.pop('user_id', None)
        return None

def login_user(user: User):
    """Log in a user (set session)"""
    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin

def logout_user():
    """Log out the current user (clear session)"""
    session.pop('user_id', None)
    session.pop('username', None) 
    session.pop('is_admin', None)
