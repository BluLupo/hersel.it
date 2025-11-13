"""
Database models for Portfolio Application
Uses SQLAlchemy ORM with MariaDB
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    """Store admin users for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Hash password using bcrypt"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Profile(db.Model):
    """Store personal profile information"""
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    lead_text = db.Column(db.Text, nullable=False)
    description_1 = db.Column(db.Text)
    description_2 = db.Column(db.Text)
    years_experience = db.Column(db.Integer, default=7)
    cv_url = db.Column(db.String(500))
    profile_image = db.Column(db.String(500), default='img/personal.webp')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'lead_text': self.lead_text,
            'description_1': self.description_1,
            'description_2': self.description_2,
            'years_experience': self.years_experience,
            'cv_url': self.cv_url,
            'profile_image': self.profile_image
        }


class Skill(db.Model):
    """Store technical skills/technologies"""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon_class = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # OS, Language, Framework, Tool, etc.
    proficiency_level = db.Column(db.Integer)  # 1-5 (optional)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon_class': self.icon_class,
            'category': self.category,
            'proficiency_level': self.proficiency_level,
            'display_order': self.display_order
        }


class Project(db.Model):
    """Store portfolio projects"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    display_order = db.Column(db.Integer, default=0)
    animation_delay = db.Column(db.String(10), default='0s')  # e.g., '0.2s'
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    tags = db.relationship('ProjectTag', backref='project', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'demo_url': self.demo_url,
            'github_url': self.github_url,
            'display_order': self.display_order,
            'animation_delay': self.animation_delay,
            'is_published': self.is_published,
            'tags': [tag.to_dict() for tag in self.tags]
        }


class ProjectTag(db.Model):
    """Store tags/badges for projects"""
    __tablename__ = 'project_tags'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color_class = db.Column(db.String(50), default='bg-primary')  # Bootstrap badge classes
    display_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color_class': self.color_class,
            'display_order': self.display_order
        }


class SocialLink(db.Model):
    """Store social media and profile links"""
    __tablename__ = 'social_links'

    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon_class = db.Column(db.String(100), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    animation_delay = db.Column(db.String(10), default='0s')  # e.g., '0.1s'
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'platform_name': self.platform_name,
            'url': self.url,
            'icon_class': self.icon_class,
            'display_order': self.display_order,
            'animation_delay': self.animation_delay
        }
