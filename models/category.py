#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Category Model

from typing import Optional, Dict, List
from .database import db_manager
from datetime import datetime

class Category:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.slug = kwargs.get('slug')
        self.description = kwargs.get('description')
        self.color = kwargs.get('color', '#007bff')
        self.created_at = kwargs.get('created_at')
    
    async def save(self) -> int:
        """Save category to database"""
        if self.id:
            # Update existing category
            query = """
                UPDATE categories SET 
                name=%s, slug=%s, description=%s, color=%s
                WHERE id=%s
            """
            params = (self.name, self.slug, self.description, self.color, self.id)
            await db_manager.execute_update(query, params)
            return self.id
        else:
            # Insert new category
            query = """
                INSERT INTO categories (name, slug, description, color)
                VALUES (%s, %s, %s, %s)
            """
            params = (self.name, self.slug, self.description, self.color)
            category_id = await db_manager.execute_insert(query, params)
            self.id = category_id
            return category_id
    
    @classmethod
    async def find_by_id(cls, category_id: int) -> Optional['Category']:
        """Find category by ID"""
        query = "SELECT * FROM categories WHERE id = %s"
        results = await db_manager.execute_query(query, (category_id,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def find_by_slug(cls, slug: str) -> Optional['Category']:
        """Find category by slug"""
        query = "SELECT * FROM categories WHERE slug = %s"
        results = await db_manager.execute_query(query, (slug,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def get_all(cls, limit: int = 50) -> List['Category']:
        """Get all categories"""
        query = "SELECT * FROM categories ORDER BY name ASC LIMIT %s"
        results = await db_manager.execute_query(query, (limit,))
        return [cls(**row) for row in results]
    
    @classmethod
    async def count(cls) -> int:
        """Count total categories"""
        query = "SELECT COUNT(*) as count FROM categories"
        results = await db_manager.execute_query(query)
        return results[0]['count'] if results else 0
    
    async def delete(self) -> bool:
        """Delete category"""
        query = "DELETE FROM categories WHERE id = %s"
        affected = await db_manager.execute_update(query, (self.id,))
        return affected > 0
    
    def to_dict(self) -> Dict:
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def generate_slug(name: str) -> str:
        """Generate URL-friendly slug from name"""
        import re
        slug = re.sub(r'[^\w\s-]', '', name).strip().lower()
        slug = re.sub(r'[\s_-]+', '-', slug)
        return slug
