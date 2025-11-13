#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

"""
Admin dashboard routes for managing portfolio content
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Profile, Skill, Project, ProjectTag, SocialLink

route_admin = Blueprint('admin', __name__, url_prefix='/admin')


@route_admin.route('/')
@login_required
def dashboard():
    """Admin dashboard home"""
    # Statistiche
    stats = {
        'projects': Project.query.count(),
        'skills': Skill.query.count(),
        'social_links': SocialLink.query.count(),
        'published_projects': Project.query.filter_by(is_published=True).count()
    }
    return render_template('admin/dashboard.html', stats=stats)


# ============================================================================
# PROFILE MANAGEMENT
# ============================================================================

@route_admin.route('/profile')
@login_required
def profile_manage():
    """Manage profile information"""
    profile = Profile.query.first()
    return render_template('admin/profile.html', profile=profile)


@route_admin.route('/profile/edit', methods=['POST'])
@login_required
def profile_edit():
    """Edit profile information"""
    profile = Profile.query.first()
    if not profile:
        flash('Profilo non trovato.', 'danger')
        return redirect(url_for('admin.profile_manage'))

    profile.title = request.form.get('title', profile.title)
    profile.lead_text = request.form.get('lead_text', profile.lead_text)
    profile.description_1 = request.form.get('description_1', profile.description_1)
    profile.description_2 = request.form.get('description_2', profile.description_2)
    profile.years_experience = int(request.form.get('years_experience', profile.years_experience))
    profile.cv_url = request.form.get('cv_url', profile.cv_url)

    db.session.commit()
    flash('Profilo aggiornato con successo!', 'success')
    return redirect(url_for('admin.profile_manage'))


# ============================================================================
# SKILLS MANAGEMENT
# ============================================================================

@route_admin.route('/skills')
@login_required
def skills_manage():
    """Manage skills"""
    skills = Skill.query.order_by(Skill.display_order).all()
    return render_template('admin/skills.html', skills=skills)


@route_admin.route('/skills/add', methods=['POST'])
@login_required
def skill_add():
    """Add new skill"""
    skill = Skill(
        name=request.form.get('name'),
        icon_class=request.form.get('icon_class'),
        category=request.form.get('category'),
        display_order=int(request.form.get('display_order', 0)),
        is_active=request.form.get('is_active') == 'on'
    )
    db.session.add(skill)
    db.session.commit()
    flash('Skill aggiunta con successo!', 'success')
    return redirect(url_for('admin.skills_manage'))


@route_admin.route('/skills/<int:skill_id>/edit', methods=['POST'])
@login_required
def skill_edit(skill_id):
    """Edit skill"""
    skill = Skill.query.get_or_404(skill_id)
    skill.name = request.form.get('name', skill.name)
    skill.icon_class = request.form.get('icon_class', skill.icon_class)
    skill.category = request.form.get('category', skill.category)
    skill.display_order = int(request.form.get('display_order', skill.display_order))
    skill.is_active = request.form.get('is_active') == 'on'

    db.session.commit()
    flash('Skill aggiornata con successo!', 'success')
    return redirect(url_for('admin.skills_manage'))


@route_admin.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def skill_delete(skill_id):
    """Delete skill"""
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill eliminata con successo!', 'success')
    return redirect(url_for('admin.skills_manage'))


# ============================================================================
# PROJECTS MANAGEMENT
# ============================================================================

@route_admin.route('/projects')
@login_required
def projects_manage():
    """Manage projects"""
    projects = Project.query.order_by(Project.display_order).all()
    return render_template('admin/projects.html', projects=projects)


@route_admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def project_add():
    """Add new project"""
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url'),
            demo_url=request.form.get('demo_url'),
            github_url=request.form.get('github_url'),
            display_order=int(request.form.get('display_order', 0)),
            animation_delay=request.form.get('animation_delay', '0s'),
            is_published=request.form.get('is_published') == 'on'
        )
        db.session.add(project)
        db.session.flush()

        # Aggiungi tags
        tags_input = request.form.get('tags', '')
        if tags_input:
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for idx, tag_name in enumerate(tags_list):
                # Estrai colore se specificato (formato: "Python:bg-primary")
                if ':' in tag_name:
                    tag_name, color = tag_name.split(':', 1)
                else:
                    color = 'bg-primary'

                tag = ProjectTag(
                    project_id=project.id,
                    name=tag_name.strip(),
                    color_class=color.strip(),
                    display_order=idx
                )
                db.session.add(tag)

        db.session.commit()
        flash('Progetto aggiunto con successo!', 'success')
        return redirect(url_for('admin.projects_manage'))

    return render_template('admin/project_form.html', project=None)


@route_admin.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def project_edit(project_id):
    """Edit project"""
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form.get('title', project.title)
        project.description = request.form.get('description', project.description)
        project.image_url = request.form.get('image_url', project.image_url)
        project.demo_url = request.form.get('demo_url', project.demo_url)
        project.github_url = request.form.get('github_url', project.github_url)
        project.display_order = int(request.form.get('display_order', project.display_order))
        project.animation_delay = request.form.get('animation_delay', project.animation_delay)
        project.is_published = request.form.get('is_published') == 'on'

        # Aggiorna tags
        ProjectTag.query.filter_by(project_id=project.id).delete()

        tags_input = request.form.get('tags', '')
        if tags_input:
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for idx, tag_name in enumerate(tags_list):
                if ':' in tag_name:
                    tag_name, color = tag_name.split(':', 1)
                else:
                    color = 'bg-primary'

                tag = ProjectTag(
                    project_id=project.id,
                    name=tag_name.strip(),
                    color_class=color.strip(),
                    display_order=idx
                )
                db.session.add(tag)

        db.session.commit()
        flash('Progetto aggiornato con successo!', 'success')
        return redirect(url_for('admin.projects_manage'))

    return render_template('admin/project_form.html', project=project)


@route_admin.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def project_delete(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Progetto eliminato con successo!', 'success')
    return redirect(url_for('admin.projects_manage'))


# ============================================================================
# SOCIAL LINKS MANAGEMENT
# ============================================================================

@route_admin.route('/social-links')
@login_required
def social_links_manage():
    """Manage social links"""
    social_links = SocialLink.query.order_by(SocialLink.display_order).all()
    return render_template('admin/social_links.html', social_links=social_links)


@route_admin.route('/social-links/add', methods=['POST'])
@login_required
def social_link_add():
    """Add new social link"""
    link = SocialLink(
        platform_name=request.form.get('platform_name'),
        url=request.form.get('url'),
        icon_class=request.form.get('icon_class'),
        display_order=int(request.form.get('display_order', 0)),
        animation_delay=request.form.get('animation_delay', '0s'),
        is_active=request.form.get('is_active') == 'on'
    )
    db.session.add(link)
    db.session.commit()
    flash('Link social aggiunto con successo!', 'success')
    return redirect(url_for('admin.social_links_manage'))


@route_admin.route('/social-links/<int:link_id>/edit', methods=['POST'])
@login_required
def social_link_edit(link_id):
    """Edit social link"""
    link = SocialLink.query.get_or_404(link_id)
    link.platform_name = request.form.get('platform_name', link.platform_name)
    link.url = request.form.get('url', link.url)
    link.icon_class = request.form.get('icon_class', link.icon_class)
    link.display_order = int(request.form.get('display_order', link.display_order))
    link.animation_delay = request.form.get('animation_delay', link.animation_delay)
    link.is_active = request.form.get('is_active') == 'on'

    db.session.commit()
    flash('Link social aggiornato con successo!', 'success')
    return redirect(url_for('admin.social_links_manage'))


@route_admin.route('/social-links/<int:link_id>/delete', methods=['POST'])
@login_required
def social_link_delete(link_id):
    """Delete social link"""
    link = SocialLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link social eliminato con successo!', 'success')
    return redirect(url_for('admin.social_links_manage'))
