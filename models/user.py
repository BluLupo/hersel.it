#!/usr/bin/env python
# -*- coding: utf-8 -*-

# User Model

import bcrypt
from typing import Optional, Dict, List
from .database import db_manager
from datetime import datetime

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password_hash = kwargs.get('password_hash')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.role = kwargs.get('role', 'user')
        self.is_active = kwargs.get('is_active', True)
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == 'admin'
    
    def set_password(self, password: str) -> None:
        """Hash and set user password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    async def save(self) -> int:
        """Save user to database"""
        if self.id:
            # Update existing user
            query = """
                UPDATE users SET 
                username=%s, email=%s, first_name=%s, last_name=%s, 
                role=%s, is_active=%s, updated_at=NOW()
                WHERE id=%s
            """
            params = (self.username, self.email, self.first_name, self.last_name, 
                     self.role, self.is_active, self.id)
            await db_manager.execute_update(query, params)
            return self.id
        else:
            # Insert new user
            query = """
                INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.username, self.email, self.password_hash, self.first_name, 
                     self.last_name, self.role, self.is_active)
            user_id = await db_manager.execute_insert(query, params)
            self.id = user_id
            return user_id
    
    @classmethod
    async def find_by_id(cls, user_id: int) -> Optional['User']:
        """Find user by ID"""
        query = "SELECT * FROM users WHERE id = %s AND is_active = TRUE"
        results = await db_manager.execute_query(query, (user_id,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def find_by_username(cls, username: str) -> Optional['User']:
        """Find user by username"""
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        results = await db_manager.execute_query(query, (username,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def find_by_email(cls, email: str) -> Optional['User']:
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        results = await db_manager.execute_query(query, (email,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def authenticate(cls, username_or_email: str, password: str) -> Optional['User']:
        """Authenticate user with username/email and password"""
        # Try to find by username first, then by email
        user = await cls.find_by_username(username_or_email)
        if not user:
            user = await cls.find_by_email(username_or_email)
        
        if user and user.check_password(password):
            return user
        return None
    
    @classmethod
    async def get_all(cls, limit: int = 50, offset: int = 0) -> List['User']:
        """Get all users with pagination"""
        query = """
            SELECT * FROM users 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        results = await db_manager.execute_query(query, (limit, offset))
        return [cls(**row) for row in results]
    
    @classmethod
    async def count(cls) -> int:
        """Count total users"""
        query = "SELECT COUNT(*) as count FROM users WHERE is_active = TRUE"
        results = await db_manager.execute_query(query)
        return results[0]['count'] if results else 0
    
    async def delete(self) -> bool:
        """Soft delete user (mark as inactive)"""
        query = "UPDATE users SET is_active = FALSE WHERE id = %s"
        affected = await db_manager.execute_update(query, (self.id,))
        return affected > 0
    
    def to_dict(self, include_sensitive: bool = False) -> Dict:
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
        
        return data
