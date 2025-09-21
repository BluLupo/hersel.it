#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella
# Home Routes

from quart import Blueprint, render_template
from models.project import Project
from models.settings import Settings

# Blueprint with correct name
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
async def index():
    """Homepage with featured projects"""
    # Get featured projects
    featured_projects = await Project.get_featured(limit=6)
    
    # Get site settings
    site_name = await Settings.get('site_name', 'Hersel.it')
    site_description = await Settings.get('site_description', 'Portfolio personale di Hersel Giannella')
    
    return await render_template('home/index.html', 
                               featured_projects=featured_projects,
                               site_name=site_name,
                               site_description=site_description)

@home_bp.route('/progetti')
async def projects():
    """Projects page"""
    # Get all published projects
    projects = await Project.get_all(published_only=True, limit=50)
    
    return await render_template('home/projects.html', projects=projects)

@home_bp.route('/progetto/<slug>')
async def project_detail(slug):
    """Single project page"""
    project = await Project.find_by_slug(slug)
    if not project:
        return await render_template('errors/404.html'), 404
    
    return await render_template('home/project_detail.html', project=project)

@home_bp.route('/about')
async def about():
    """About page"""
    return await render_template('home/about.html')

@home_bp.route('/contatti')
async def contact():
    """Contact page"""
    return await render_template('home/contact.html')

# Keep backward compatibility
route_home = home_bp
