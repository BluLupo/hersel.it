#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Validation Utilities

import re
from typing import Tuple, Optional

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email format"""
    if not email:
        return False, "Email è richiesta"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Formato email non valido"
    
    if len(email) > 100:
        return False, "Email troppo lunga (max 100 caratteri)"
    
    return True, None

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password strength"""
    if not password:
        return False, "Password è richiesta"
    
    if len(password) < 8:
        return False, "Password deve essere almeno 8 caratteri"
    
    if len(password) > 128:
        return False, "Password troppo lunga (max 128 caratteri)"
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password deve contenere almeno una lettera maiuscola"
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password deve contenere almeno una lettera minuscola"
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password deve contenere almeno un numero"
    
    return True, None

def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """Validate username format"""
    if not username:
        return False, "Username è richiesto"
    
    if len(username) < 3:
        return False, "Username deve essere almeno 3 caratteri"
    
    if len(username) > 50:
        return False, "Username troppo lungo (max 50 caratteri)"
    
    # Check for valid characters (alphanumeric and underscore)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username può contenere solo lettere, numeri e underscore"
    
    return True, None

def validate_project_data(data: dict) -> Tuple[bool, dict]:
    """Validate project data"""
    errors = {}
    
    # Title validation
    if not data.get('title', '').strip():
        errors['title'] = 'Titolo è richiesto'
    elif len(data['title']) > 200:
        errors['title'] = 'Titolo troppo lungo (max 200 caratteri)'
    
    # Description validation
    if data.get('description') and len(data['description']) > 1000:
        errors['description'] = 'Descrizione troppo lunga (max 1000 caratteri)'
    
    # URL validations
    url_pattern = r'^https?://[^\s]+$'
    
    if data.get('github_url') and not re.match(url_pattern, data['github_url']):
        errors['github_url'] = 'URL GitHub non valido'
    
    if data.get('demo_url') and not re.match(url_pattern, data['demo_url']):
        errors['demo_url'] = 'URL Demo non valido'
    
    if data.get('image_url') and not re.match(url_pattern, data['image_url']):
        errors['image_url'] = 'URL Immagine non valido'
    
    return len(errors) == 0, errors

def validate_post_data(data: dict) -> Tuple[bool, dict]:
    """Validate blog post data"""
    errors = {}
    
    # Title validation
    if not data.get('title', '').strip():
        errors['title'] = 'Titolo è richiesto'
    elif len(data['title']) > 200:
        errors['title'] = 'Titolo troppo lungo (max 200 caratteri)'
    
    # Content validation
    if not data.get('content', '').strip():
        errors['content'] = 'Contenuto è richiesto'
    
    # Excerpt validation
    if data.get('excerpt') and len(data['excerpt']) > 500:
        errors['excerpt'] = 'Riassunto troppo lungo (max 500 caratteri)'
    
    return len(errors) == 0, errors
