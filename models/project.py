#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project Model

import json
from typing import Optional, Dict, List
from .database import db_manager
from datetime import datetime

class Project:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.slug = kwargs.get('slug')
        self.description = kwargs.get('description')
        self.content = kwargs.get('content')
        self.image_url = kwargs.get('image_url')
        self.github_url = kwargs.get('github_url')
        self.demo_url = kwargs.get('demo_url')
        self.technologies = kwargs.get('technologies', [])
        self.category_id = kwargs.get('category_id')
        self.is_featured = kwargs.get('is_featured', False)
        self.is_published = kwargs.get('is_published', True)
        self.created_by = kwargs.get('created_by')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')
        
        # Handle JSON technologies field
        if isinstance(self.technologies, str):
            try:
                self.technologies = json.loads(self.technologies)
            except:
                self.technologies = []
    
    @property
    def technologies_json(self) -> str:
        """Get technologies as JSON string"""
        return json.dumps(self.technologies) if self.technologies else '[]'
    
    async def save(self) -> int:
        """Save project to database"""
        if self.id:
            # Update existing project
            query = """
                UPDATE projects SET 
                title=%s, slug=%s, description=%s, content=%s, image_url=%s,
                github_url=%s, demo_url=%s, technologies=%s, category_id=%s,
                is_featured=%s, is_published=%s, updated_at=NOW()
                WHERE id=%s
            """
            params = (self.title, self.slug, self.description, self.content, self.image_url,
                     self.github_url, self.demo_url, self.technologies_json, self.category_id,
                     self.is_featured, self.is_published, self.id)
            await db_manager.execute_update(query, params)
            return self.id
        else:
            # Insert new project
            query = """
                INSERT INTO projects (title, slug, description, content, image_url, github_url, demo_url, 
                                    technologies, category_id, is_featured, is_published, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.title, self.slug, self.description, self.content, self.image_url,
                     self.github_url, self.demo_url, self.technologies_json, self.category_id,
                     self.is_featured, self.is_published, self.created_by)
            project_id = await db_manager.execute_insert(query, params)
            self.id = project_id
            return project_id
    
    @classmethod
    async def find_by_id(cls, project_id: int) -> Optional['Project']:
        """Find project by ID"""
        query = "SELECT * FROM projects WHERE id = %s"
        results = await db_manager.execute_query(query, (project_id,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def find_by_slug(cls, slug: str) -> Optional['Project']:
        """Find project by slug"""
        query = "SELECT * FROM projects WHERE slug = %s AND is_published = TRUE"
        results = await db_manager.execute_query(query, (slug,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    async def get_all(cls, published_only: bool = True, limit: int = 50, offset: int = 0) -> List['Project']:
        """Get all projects with pagination"""
        query = "SELECT * FROM projects"
        params = []
        
        if published_only:
            query += " WHERE is_published = TRUE"
        
        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        results = await db_manager.execute_query(query, tuple(params))
        return [cls(**row) for row in results]
    
    @classmethod
    async def get_featured(cls, limit: int = 6) -> List['Project']:
        """Get featured projects"""
        query = """
            SELECT * FROM projects 
            WHERE is_published = TRUE AND is_featured = TRUE 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        results = await db_manager.execute_query(query, (limit,))
        return [cls(**row) for row in results]
    
    @classmethod
    async def get_by_category(cls, category_id: int, limit: int = 20) -> List['Project']:
        """Get projects by category"""
        query = """
            SELECT * FROM projects 
            WHERE category_id = %s AND is_published = TRUE 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        results = await db_manager.execute_query(query, (category_id, limit))
        return [cls(**row) for row in results]
    
    @classmethod
    async def search(cls, search_term: str, limit: int = 20) -> List['Project']:
        """Search projects by title and description"""
        query = """
            SELECT * FROM projects 
            WHERE (title LIKE %s OR description LIKE %s) AND is_published = TRUE 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        search_pattern = f"%{search_term}%"
        results = await db_manager.execute_query(query, (search_pattern, search_pattern, limit))
        return [cls(**row) for row in results]
    
    @classmethod
    async def count(cls, published_only: bool = True) -> int:
        """Count total projects"""
        query = "SELECT COUNT(*) as count FROM projects"
        if published_only:
            query += " WHERE is_published = TRUE"
        
        results = await db_manager.execute_query(query)
        return results[0]['count'] if results else 0
    
    async def delete(self) -> bool:
        """Delete project"""
        query = "DELETE FROM projects WHERE id = %s"
        affected = await db_manager.execute_update(query, (self.id,))
        return affected > 0
    
    def to_dict(self) -> Dict:
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'content': self.content,
            'image_url': self.image_url,
            'github_url': self.github_url,
            'demo_url': self.demo_url,
            'technologies': self.technologies,
            'category_id': self.category_id,
            'is_featured': self.is_featured,
            'is_published': self.is_published,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def generate_slug(title: str) -> str:
        """Generate URL-friendly slug from title"""
        import re
        slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
        slug = re.sub(r'[\s_-]+', '-', slug)
        return slug
