#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template
from models import Profile, Skill, Project, SocialLink

route_home = Blueprint('route_home', __name__)

@route_home.route('/')
def home():
    """Render home page with dynamic data from database"""
    # Fetch all data from database
    profile = Profile.query.first()
    skills = Skill.query.filter_by(is_active=True).order_by(Skill.display_order).all()
    projects = Project.query.filter_by(is_published=True).order_by(Project.display_order).all()
    social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.display_order).all()

    return render_template(
        'index.html',
        profile=profile,
        skills=skills,
        projects=projects,
        social_links=social_links
    )
