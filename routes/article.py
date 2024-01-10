#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template
from database.methods.articles import get_article_by_id

route_article = Blueprint('route_article', __name__)

@route_article.route('/article/<int:article_id>', methods=['GET', 'POST'])
def view_article(article_id):
    article = get_article_by_id(article_id)
    return render_template('article.html',article=article)