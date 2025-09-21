#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Settings Model

import json
from typing import Optional, Dict, List, Any
from .database import db_manager

class Settings:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.setting_key = kwargs.get('setting_key')
        self.setting_value = kwargs.get('setting_value')
        self.description = kwargs.get('description')
        self.type = kwargs.get('type', 'text')
        self.updated_at = kwargs.get('updated_at')
    
    @property
    def parsed_value(self) -> Any:
        """Parse setting value based on type"""
        if not self.setting_value:
            return None
        
        if self.type == 'boolean':
            return self.setting_value.lower() in ('true', '1', 'yes', 'on')
        elif self.type == 'json':
            try:
                return json.loads(self.setting_value)
            except:
                return {}
        else:
            return self.setting_value
    
    async def save(self) -> int:
        """Save setting to database"""
        if self.id:
            # Update existing setting
            query = """
                UPDATE settings SET 
                setting_key=%s, setting_value=%s, description=%s, type=%s, updated_at=NOW()
                WHERE id=%s
            """
            params = (self.setting_key, self.setting_value, self.description, self.type, self.id)
            await db_manager.execute_update(query, params)
            return self.id
        else:
            # Insert new setting
            query = """
                INSERT INTO settings (setting_key, setting_value, description, type)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                setting_value=VALUES(setting_value), 
                description=VALUES(description), 
                type=VALUES(type),
                updated_at=NOW()
            """
            params = (self.setting_key, self.setting_value, self.description, self.type)
            setting_id = await db_manager.execute_insert(query, params)
            self.id = setting_id or self.id
            return self.id
    
    @classmethod
    async def get(cls, key: str, default: Any = None) -> Any:
        """Get setting value by key"""
        query = "SELECT * FROM settings WHERE setting_key = %s"
        results = await db_manager.execute_query(query, (key,))
        if results:
            setting = cls(**results[0])
            return setting.parsed_value
        return default
    
    @classmethod
    async def set(cls, key: str, value: Any, description: str = '', setting_type: str = 'text') -> bool:
        """Set setting value"""
        # Convert value to string based on type
        if setting_type == 'boolean':
            str_value = 'true' if value else 'false'
        elif setting_type == 'json':
            str_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        else:
            str_value = str(value)
        
        setting = cls(
            setting_key=key,
            setting_value=str_value,
            description=description,
            type=setting_type
        )
        
        try:
            await setting.save()
            return True
        except:
            return False
    
    @classmethod
    async def get_all(cls) -> List['Settings']:
        """Get all settings"""
        query = "SELECT * FROM settings ORDER BY setting_key ASC"
        results = await db_manager.execute_query(query)
        return [cls(**row) for row in results]
    
    @classmethod
    async def get_by_prefix(cls, prefix: str) -> List['Settings']:
        """Get settings by key prefix"""
        query = "SELECT * FROM settings WHERE setting_key LIKE %s ORDER BY setting_key ASC"
        results = await db_manager.execute_query(query, (f"{prefix}%",))
        return [cls(**row) for row in results]
    
    async def delete(self) -> bool:
        """Delete setting"""
        query = "DELETE FROM settings WHERE id = %s"
        affected = await db_manager.execute_update(query, (self.id,))
        return affected > 0
    
    def to_dict(self) -> Dict:
        """Convert setting to dictionary"""
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.setting_value,
            'parsed_value': self.parsed_value,
            'description': self.description,
            'type': self.type,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
