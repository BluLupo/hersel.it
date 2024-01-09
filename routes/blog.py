#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template
from database.methods.articles import get_articles_and_authors_raw, get_article_by_id
#from flask_paginate import Pagination, get_page_args

route_blog = Blueprint('route_blog', __name__)

@route_blog.route('/blog', methods=['GET', 'POST'])
def blog():
    # Chiamata alla funzione
    articles_and_authors = get_articles_and_authors_raw()
    get_article = get_article_by_id(1)
    print(get_article)
    print(articles_and_authors)

    # Cicla e stampa ogni articolo
    for article in articles_and_authors:
        print(article['title'])
    #print(b)
    return render_template('blog.html',articles=articles_and_authors)