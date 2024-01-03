#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template

route_blog = Blueprint('route_blog', __name__)

@route_blog.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html')