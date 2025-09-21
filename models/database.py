#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Database Configuration and Connection Manager

import asyncio
import aiomysql
from typing import Optional
from config import config

class DatabaseManager:
    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None
    
    async def init_pool(self):
        """Initialize connection pool"""
        try:
            self.pool = await aiomysql.create_pool(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                db=config.DB_NAME,
                minsize=1,
                maxsize=10,
                autocommit=True,
                charset='utf8mb4'
            )
            print("✅ Database connection pool initialized")
        except Exception as e:
            print(f"❌ Error initializing database pool: {e}")
            raise
    
    async def close_pool(self):
        """Close connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("🔒 Database connection pool closed")
    
    async def get_connection(self):
        """Get connection from pool"""
        if not self.pool:
            await self.init_pool()
        return self.pool.acquire()
    
    async def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchall()
    
    async def execute_insert(self, query: str, params: tuple = None):
        """Execute insert query and return last insert id"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                return cursor.lastrowid
    
    async def execute_update(self, query: str, params: tuple = None):
        """Execute update/delete query and return affected rows"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                return cursor.rowcount

# Global database manager instance
db_manager = DatabaseManager()

async def init_database():
    """Initialize database and create tables"""
    await db_manager.init_pool()
    await create_tables()

async def create_tables():
    """Create database tables if they don't exist"""
    tables = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            role ENUM('admin', 'user') DEFAULT 'user',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
        
        # Categories table
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            color VARCHAR(7) DEFAULT '#007bff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
        
        # Projects table
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            description TEXT,
            content LONGTEXT,
            image_url VARCHAR(500),
            github_url VARCHAR(500),
            demo_url VARCHAR(500),
            technologies JSON,
            category_id INT,
            is_featured BOOLEAN DEFAULT FALSE,
            is_published BOOLEAN DEFAULT TRUE,
            created_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
        
        # Posts table (for blog functionality)
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            excerpt TEXT,
            content LONGTEXT,
            featured_image VARCHAR(500),
            category_id INT,
            author_id INT,
            is_published BOOLEAN DEFAULT FALSE,
            published_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """,
        
        # Settings table
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            setting_key VARCHAR(100) UNIQUE NOT NULL,
            setting_value LONGTEXT,
            description TEXT,
            type ENUM('text', 'textarea', 'boolean', 'json') DEFAULT 'text',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """
    ]
    
    for table_sql in tables:
        try:
            await db_manager.execute_update(table_sql)
            print(f"✅ Table created/verified")
        except Exception as e:
            print(f"❌ Error creating table: {e}")
    
    # Insert default settings
    await insert_default_settings()
    
async def insert_default_settings():
    """Insert default settings if they don't exist"""
    default_settings = [
        ('site_name', 'Hersel.it', 'Nome del sito', 'text'),
        ('site_description', 'Portfolio personale di Hersel Giannella', 'Descrizione del sito', 'textarea'),
        ('admin_email', 'admin@hersel.it', 'Email amministratore', 'text'),
        ('site_logo', '/static/img/logo.png', 'URL del logo', 'text'),
        ('social_github', 'https://github.com/BluLupo', 'GitHub URL', 'text'),
        ('social_linkedin', '', 'LinkedIn URL', 'text'),
        ('social_twitter', '', 'Twitter URL', 'text'),
        ('site_maintenance', 'false', 'Modalità manutenzione', 'boolean'),
        ('analytics_code', '', 'Codice Analytics', 'textarea')
    ]
    
    for key, value, desc, type_val in default_settings:
        try:
            await db_manager.execute_insert(
                "INSERT IGNORE INTO settings (setting_key, setting_value, description, type) VALUES (%s, %s, %s, %s)",
                (key, value, desc, type_val)
            )
        except Exception as e:
            print(f"Warning: Could not insert setting {key}: {e}")
