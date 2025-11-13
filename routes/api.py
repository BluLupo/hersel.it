#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

"""
API Routes for managing portfolio data dynamically
Provides REST endpoints for CRUD operations on Profile, Skills, Projects, and Social Links
All write operations (POST, PUT, DELETE) require authentication
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import db, Profile, Skill, Project, ProjectTag, SocialLink

route_api = Blueprint('api', __name__, url_prefix='/api')


# ============================================================================
# PROFILE ENDPOINTS
# ============================================================================

@route_api.route('/profile', methods=['GET'])
def get_profile():
    """Get profile information"""
    profile = Profile.query.first()
    if profile:
        return jsonify(profile.to_dict())
    return jsonify({'message': 'Profile not found'}), 404


@route_api.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update profile information"""
    profile = Profile.query.first()
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    data = request.json
    profile.title = data.get('title', profile.title)
    profile.lead_text = data.get('lead_text', profile.lead_text)
    profile.description_1 = data.get('description_1', profile.description_1)
    profile.description_2 = data.get('description_2', profile.description_2)
    profile.years_experience = data.get('years_experience', profile.years_experience)
    profile.cv_url = data.get('cv_url', profile.cv_url)

    db.session.commit()
    return jsonify(profile.to_dict())


# ============================================================================
# SKILLS ENDPOINTS
# ============================================================================

@route_api.route('/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    skills = Skill.query.order_by(Skill.display_order).all()
    return jsonify([skill.to_dict() for skill in skills])


@route_api.route('/skills', methods=['POST'])
@login_required
def create_skill():
    """Create a new skill"""
    data = request.json
    skill = Skill(
        name=data['name'],
        icon_class=data['icon_class'],
        category=data.get('category'),
        proficiency_level=data.get('proficiency_level'),
        display_order=data.get('display_order', 0),
        is_active=data.get('is_active', True)
    )
    db.session.add(skill)
    db.session.commit()
    return jsonify(skill.to_dict()), 201


@route_api.route('/skills/<int:skill_id>', methods=['PUT'])
@login_required
def update_skill(skill_id):
    """Update a skill"""
    skill = Skill.query.get_or_404(skill_id)
    data = request.json

    skill.name = data.get('name', skill.name)
    skill.icon_class = data.get('icon_class', skill.icon_class)
    skill.category = data.get('category', skill.category)
    skill.proficiency_level = data.get('proficiency_level', skill.proficiency_level)
    skill.display_order = data.get('display_order', skill.display_order)
    skill.is_active = data.get('is_active', skill.is_active)

    db.session.commit()
    return jsonify(skill.to_dict())


@route_api.route('/skills/<int:skill_id>', methods=['DELETE'])
@login_required
def delete_skill(skill_id):
    """Delete a skill"""
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': 'Skill deleted successfully'})


# ============================================================================
# PROJECTS ENDPOINTS
# ============================================================================

@route_api.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    projects = Project.query.order_by(Project.display_order).all()
    return jsonify([project.to_dict() for project in projects])


@route_api.route('/projects', methods=['POST'])
@login_required
def create_project():
    """Create a new project"""
    data = request.json
    project = Project(
        title=data['title'],
        description=data['description'],
        image_url=data.get('image_url'),
        demo_url=data.get('demo_url'),
        github_url=data.get('github_url'),
        display_order=data.get('display_order', 0),
        animation_delay=data.get('animation_delay', '0s'),
        is_published=data.get('is_published', True)
    )
    db.session.add(project)
    db.session.flush()

    # Add tags
    tags_data = data.get('tags', [])
    for tag_data in tags_data:
        tag = ProjectTag(
            project_id=project.id,
            name=tag_data['name'],
            color_class=tag_data.get('color_class', 'bg-primary'),
            display_order=tag_data.get('display_order', 0)
        )
        db.session.add(tag)

    db.session.commit()
    return jsonify(project.to_dict()), 201


@route_api.route('/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    """Update a project"""
    project = Project.query.get_or_404(project_id)
    data = request.json

    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.image_url = data.get('image_url', project.image_url)
    project.demo_url = data.get('demo_url', project.demo_url)
    project.github_url = data.get('github_url', project.github_url)
    project.display_order = data.get('display_order', project.display_order)
    project.animation_delay = data.get('animation_delay', project.animation_delay)
    project.is_published = data.get('is_published', project.is_published)

    # Update tags if provided
    if 'tags' in data:
        # Remove old tags
        ProjectTag.query.filter_by(project_id=project.id).delete()
        # Add new tags
        for tag_data in data['tags']:
            tag = ProjectTag(
                project_id=project.id,
                name=tag_data['name'],
                color_class=tag_data.get('color_class', 'bg-primary'),
                display_order=tag_data.get('display_order', 0)
            )
            db.session.add(tag)

    db.session.commit()
    return jsonify(project.to_dict())


@route_api.route('/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'})


# ============================================================================
# SOCIAL LINKS ENDPOINTS
# ============================================================================

@route_api.route('/social-links', methods=['GET'])
def get_social_links():
    """Get all social links"""
    links = SocialLink.query.order_by(SocialLink.display_order).all()
    return jsonify([link.to_dict() for link in links])


@route_api.route('/social-links', methods=['POST'])
@login_required
def create_social_link():
    """Create a new social link"""
    data = request.json
    link = SocialLink(
        platform_name=data['platform_name'],
        url=data['url'],
        icon_class=data['icon_class'],
        display_order=data.get('display_order', 0),
        animation_delay=data.get('animation_delay', '0s'),
        is_active=data.get('is_active', True)
    )
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201


@route_api.route('/social-links/<int:link_id>', methods=['PUT'])
@login_required
def update_social_link(link_id):
    """Update a social link"""
    link = SocialLink.query.get_or_404(link_id)
    data = request.json

    link.platform_name = data.get('platform_name', link.platform_name)
    link.url = data.get('url', link.url)
    link.icon_class = data.get('icon_class', link.icon_class)
    link.display_order = data.get('display_order', link.display_order)
    link.animation_delay = data.get('animation_delay', link.animation_delay)
    link.is_active = data.get('is_active', link.is_active)

    db.session.commit()
    return jsonify(link.to_dict())


@route_api.route('/social-links/<int:link_id>', methods=['DELETE'])
@login_required
def delete_social_link(link_id):
    """Delete a social link"""
    link = SocialLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({'message': 'Social link deleted successfully'})
