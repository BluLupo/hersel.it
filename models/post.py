#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Post Model (for future blog functionality)

from typing import Optional, Dict, List
from .database import db_manager
from datetime import datetime

class Post:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.slug = kwargs.get('slug')
        self.excerpt = kwargs.get('excerpt')
        self.content = kwargs.get('content')
        self.featured_image = kwargs.get('featured_image')
        self.category_id = kwargs.get('category_id')
        self.author_id = kwargs.get('author_id')
        self.is_published = kwargs.get('is_published', False)
        self.published_at = kwargs.get('published_at')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
    
    async def save(self) -> int:
        """Save post to database"""
        if self.id:
            # Update existing post
            query = """
                UPDATE posts SET 
                title=%s, slug=%s, excerpt=%s, content=%s, featured_image=%s,
                category_id=%s, is_published=%s, published_at=%s, updated_at=NOW()
                WHERE id=%s
            """
            params = (self.title, self.slug, self.excerpt, self.content, self.featured_image,
                     self.category_id, self.is_published, self.published_at, self.id)
            await db_manager.execute_update(query, params)
            return self.id
        else:
            # Insert new post
            query = """
                INSERT INTO posts (title, slug, excerpt, content, featured_image, category_id, 
                                 author_id, is_published, published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.title, self.slug, self.excerpt, self.content, self.featured_image,
                     self.category_id, self.author_id, self.is_published, self.published_at)
            post_id = await db_manager.execute_insert(query, params)
            self.id = post_id
            return post_id
    
    @classmethod
    async def find_by_id(cls, post_id: int) -> Optional['Post']:
        """Find post by ID"""
        query = "SELECT * FROM posts WHERE id = %s"
        results = await db_manager.execute_query(query, (post_id,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def find_by_slug(cls, slug: str) -> Optional['Post']:
        """Find post by slug"""
        query = "SELECT * FROM posts WHERE slug = %s AND is_published = TRUE"
        results = await db_manager.execute_query(query, (slug,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def get_all(cls, published_only: bool = True, limit: int = 50, offset: int = 0) -> List['Post']:
        """Get all posts with pagination"""
        query = "SELECT * FROM posts"
        params = []
        
        if published_only:
            query += " WHERE is_published = TRUE"
        
        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        results = await db_manager.execute_query(query, tuple(params))
        return [cls(**row) for row in results]
    
    @classmethod
    async def count(cls, published_only: bool = True) -> int:
        """Count total posts"""
        query = "SELECT COUNT(*) as count FROM posts"
        if published_only:
            query += " WHERE is_published = TRUE"
        
        results = await db_manager.execute_query(query)
        return results[0]['count'] if results else 0
    
    async def delete(self) -> bool:
        """Delete post"""
        query = "DELETE FROM posts WHERE id = %s"
        affected = await db_manager.execute_update(query, (self.id,))
        return affected > 0
    
    def to_dict(self) -> Dict:
        """Convert post to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'content': self.content,
            'featured_image': self.featured_image,
            'category_id': self.category_id,
            'author_id': self.author_id,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
