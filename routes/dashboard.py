#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dashboard Routes (Admin)

from quart import Blueprint, request, render_template, redirect, url_for, jsonify, session
from models.user import User
from models.project import Project
from models.category import Category
from utils.auth import admin_required, get_current_user
from utils.helpers import flash_message, generate_slug, calculate_pagination
from utils.validators import validate_project_data

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Debug route to check authentication status
@dashboard_bp.route('/debug/auth')
async def debug_auth():
    """Debug route to check authentication status"""
    current_user = await get_current_user()
    session_data = dict(session)
    
    debug_info = {
        'session_exists': 'user_id' in session,
        'user_id_in_session': session.get('user_id'),
        'username_in_session': session.get('username'),
        'is_admin_in_session': session.get('is_admin'),
        'current_user_found': current_user is not None,
        'current_user_is_admin': current_user.is_admin if current_user else None,
        'current_user_details': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role,
            'is_admin': current_user.is_admin
        } if current_user else None,
        'session_data': session_data
    }
    
    return jsonify(debug_info)

# Public route to check dashboard access without admin_required decorator
@dashboard_bp.route('/debug/access')
async def debug_access():
    """Debug route to check dashboard access requirements"""
    try:
        current_user = await get_current_user()
        
        if not current_user:
            return jsonify({
                'status': 'error',
                'message': 'Nessun utente loggato',
                'redirect': url_for('auth.login')
            }), 401
        
        if not current_user.is_admin:
            return jsonify({
                'status': 'error', 
                'message': f'Utente {current_user.username} non ha privilegi di amministratore',
                'user_role': current_user.role,
                'is_admin': current_user.is_admin,
                'redirect': url_for('home.index')
            }), 403
        
        return jsonify({
            'status': 'success',
            'message': f'Accesso consentito per {current_user.username}',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'role': current_user.role,
                'is_admin': current_user.is_admin
            },
            'dashboard_url': url_for('dashboard.index')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Errore durante il controllo accesso: {str(e)}'
        }), 500

@dashboard_bp.route('/')
@admin_required
async def index():
    """Dashboard home"""
    try:
        current_user = await get_current_user()
        
        # Get statistics with error handling
        stats = {
            'total_users': 0,
            'total_projects': 0,
            'published_projects': 0,
            'featured_projects': 0
        }
        
        try:
            stats['total_users'] = await User.count()
        except Exception as e:
            print(f"Error getting user count: {e}")
            
        try:
            stats['total_projects'] = await Project.count(published_only=False)
            stats['published_projects'] = await Project.count(published_only=True)
            featured_projects = await Project.get_featured()
            stats['featured_projects'] = len(featured_projects) if featured_projects else 0
        except Exception as e:
            print(f"Error getting project stats: {e}")
        
        # Get recent projects with error handling
        recent_projects = []
        try:
            recent_projects = await Project.get_all(published_only=False, limit=5)
        except Exception as e:
            print(f"Error getting recent projects: {e}")
        
        return await render_template('dashboard/index.html', 
                                   user=current_user, 
                                   stats=stats, 
                                   recent_projects=recent_projects)
    except Exception as e:
        flash_message(f'Errore nel caricamento della dashboard: {str(e)}', 'error')
        return redirect(url_for('home.index'))

@dashboard_bp.route('/projects')
@admin_required
async def projects():
    """Projects management"""
    page = int(request.args.get('page', 1))
    per_page = 10
    
    try:
        # Get projects with pagination
        projects = await Project.get_all(published_only=False, limit=per_page, offset=(page-1)*per_page)
        total_projects = await Project.count(published_only=False)
        
        pagination = calculate_pagination(total_projects, page, per_page)
        
        return await render_template('dashboard/projects.html', 
                                   projects=projects, 
                                   pagination=pagination)
    except Exception as e:
        flash_message(f'Errore nel caricamento dei progetti: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/projects/new', methods=['GET', 'POST'])
@admin_required
async def new_project():
    """Create new project"""
    if request.method == 'GET':
        try:
            categories = await Category.get_all()
            return await render_template('dashboard/project_form.html', 
                                       project=None, 
                                       categories=categories,
                                       action='create')
        except Exception as e:
            flash_message(f'Errore nel caricamento delle categorie: {str(e)}', 'error')
            return redirect(url_for('dashboard.projects'))
    
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
    
    try:
        users = await User.get_all(limit=per_page, offset=(page-1)*per_page)
        total_users = await User.count()
        
        pagination = calculate_pagination(total_users, page, per_page)
        
        return await render_template('dashboard/users.html', 
                                   users=users, 
                                   pagination=pagination)
    except Exception as e:
        flash_message(f'Errore nel caricamento degli utenti: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))