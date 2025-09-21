#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dashboard Routes (Admin)

from quart import Blueprint, request, render_template, redirect, url_for, jsonify
from models.user import User
from models.project import Project
from models.category import Category
from utils.auth import admin_required, get_current_user
from utils.helpers import flash_message, generate_slug, calculate_pagination
from utils.validators import validate_project_data

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@admin_required
async def index():
    """Dashboard home"""
    current_user = await get_current_user()
    
    # Get statistics
    stats = {
        'total_users': await User.count(),
        'total_projects': await Project.count(published_only=False),
        'published_projects': await Project.count(published_only=True),
        'featured_projects': len(await Project.get_featured())
    }
    
    # Get recent projects
    recent_projects = await Project.get_all(published_only=False, limit=5)
    
    return await render_template('dashboard/index.html', 
                               user=current_user, 
                               stats=stats, 
                               recent_projects=recent_projects)

@dashboard_bp.route('/projects')
@admin_required
async def projects():
    """Projects management"""
    page = int(request.args.get('page', 1))
    per_page = 10
    
    # Get projects with pagination
    projects = await Project.get_all(published_only=False, limit=per_page, offset=(page-1)*per_page)
    total_projects = await Project.count(published_only=False)
    
    pagination = calculate_pagination(total_projects, page, per_page)
    
    return await render_template('dashboard/projects.html', 
                               projects=projects, 
                               pagination=pagination)

@dashboard_bp.route('/projects/new', methods=['GET', 'POST'])
@admin_required
async def new_project():
    """Create new project"""
    if request.method == 'GET':
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=None, 
                                   categories=categories,
                                   action='create')
    
    form_data = await request.form
    data = {
        'title': form_data.get('title', '').strip(),
        'description': form_data.get('description', '').strip(),
        'content': form_data.get('content', '').strip(),
        'github_url': form_data.get('github_url', '').strip(),
        'demo_url': form_data.get('demo_url', '').strip(),
        'image_url': form_data.get('image_url', '').strip(),
        'technologies': form_data.getlist('technologies'),
        'category_id': int(form_data.get('category_id')) if form_data.get('category_id') else None,
        'is_featured': bool(form_data.get('is_featured')),
        'is_published': bool(form_data.get('is_published'))
    }
    
    # Validate data
    is_valid, errors = validate_project_data(data)
    
    if not is_valid:
        for field, error in errors.items():
            flash_message(error, 'error')
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=data, 
                                   categories=categories,
                                   action='create')
    
    # Create project
    current_user = await get_current_user()
    project = Project(
        title=data['title'],
        slug=generate_slug(data['title']),
        description=data['description'],
        content=data['content'],
        github_url=data['github_url'],
        demo_url=data['demo_url'],
        image_url=data['image_url'],
        technologies=data['technologies'],
        category_id=data['category_id'],
        is_featured=data['is_featured'],
        is_published=data['is_published'],
        created_by=current_user.id
    )
    
    try:
        await project.save()
        flash_message('Progetto creato con successo!', 'success')
        return redirect(url_for('dashboard.projects'))
    except Exception as e:
        flash_message('Errore durante la creazione del progetto', 'error')
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=data, 
                                   categories=categories,
                                   action='create')

@dashboard_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@admin_required
async def edit_project(project_id):
    """Edit project"""
    project = await Project.find_by_id(project_id)
    if not project:
        flash_message('Progetto non trovato', 'error')
        return redirect(url_for('dashboard.projects'))
    
    if request.method == 'GET':
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=project, 
                                   categories=categories,
                                   action='edit')
    
    form_data = await request.form
    data = {
        'title': form_data.get('title', '').strip(),
        'description': form_data.get('description', '').strip(),
        'content': form_data.get('content', '').strip(),
        'github_url': form_data.get('github_url', '').strip(),
        'demo_url': form_data.get('demo_url', '').strip(),
        'image_url': form_data.get('image_url', '').strip(),
        'technologies': form_data.getlist('technologies'),
        'category_id': int(form_data.get('category_id')) if form_data.get('category_id') else None,
        'is_featured': bool(form_data.get('is_featured')),
        'is_published': bool(form_data.get('is_published'))
    }
    
    # Validate data
    is_valid, errors = validate_project_data(data)
    
    if not is_valid:
        for field, error in errors.items():
            flash_message(error, 'error')
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=project, 
                                   categories=categories,
                                   action='edit')
    
    # Update project
    project.title = data['title']
    project.slug = generate_slug(data['title'])
    project.description = data['description']
    project.content = data['content']
    project.github_url = data['github_url']
    project.demo_url = data['demo_url']
    project.image_url = data['image_url']
    project.technologies = data['technologies']
    project.category_id = data['category_id']
    project.is_featured = data['is_featured']
    project.is_published = data['is_published']
    
    try:
        await project.save()
        flash_message('Progetto aggiornato con successo!', 'success')
        return redirect(url_for('dashboard.projects'))
    except Exception as e:
        flash_message('Errore durante l\'aggiornamento del progetto', 'error')
        categories = await Category.get_all()
        return await render_template('dashboard/project_form.html', 
                                   project=project, 
                                   categories=categories,
                                   action='edit')

@dashboard_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@admin_required
async def delete_project(project_id):
    """Delete project"""
    project = await Project.find_by_id(project_id)
    if not project:
        return jsonify({'error': 'Progetto non trovato'}), 404
    
    try:
        await project.delete()
        flash_message('Progetto eliminato con successo!', 'success')
        return redirect(url_for('dashboard.projects'))
    except Exception as e:
        flash_message('Errore durante l\'eliminazione del progetto', 'error')
        return redirect(url_for('dashboard.projects'))

@dashboard_bp.route('/users')
@admin_required
async def users():
    """Users management"""
    page = int(request.args.get('page', 1))
    per_page = 10
    
    users = await User.get_all(limit=per_page, offset=(page-1)*per_page)
    total_users = await User.count()
    
    pagination = calculate_pagination(total_users, page, per_page)
    
    return await render_template('dashboard/users.html', 
                               users=users, 
                               pagination=pagination)
