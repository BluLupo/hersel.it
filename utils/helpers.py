#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Helper Utilities

import re
import html
from quart import session
from typing import List

def flash_message(message: str, category: str = 'info'):
    """Add a flash message to session"""
    if 'flash_messages' not in session:
        session['flash_messages'] = []
    session['flash_messages'].append({'message': message, 'category': category})

def get_flash_messages() -> List[dict]:
    """Get and clear flash messages from session"""
    messages = session.pop('flash_messages', [])
    return messages

def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', text).strip().lower()
    slug = re.sub(r'[\s_-]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def sanitize_html(text: str) -> str:
    """Basic HTML sanitization"""
    if not text:
        return ''
    # Escape HTML entities
    return html.escape(text)

def truncate_text(text: str, max_length: int = 150, suffix: str = '...') -> str:
    """Truncate text to specified length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def format_date(date_obj, format_str: str = '%d/%m/%Y') -> str:
    """Format datetime object to string"""
    if not date_obj:
        return ''
    return date_obj.strftime(format_str)

def paginate_query_params(page: int = 1, per_page: int = 10) -> tuple:
    """Generate LIMIT and OFFSET for pagination"""
    if page < 1:
        page = 1
    offset = (page - 1) * per_page
    return per_page, offset

def calculate_pagination(total_items: int, page: int, per_page: int) -> dict:
    """Calculate pagination information"""
    total_pages = (total_items + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total_items,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': page - 1 if has_prev else None,
        'next_page': page + 1 if has_next else None
    }
