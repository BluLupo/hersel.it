#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_args
from database.methods.articles import get_articles_and_authors_raw, get_article_by_id
from utilities.aboutclass import BluLupo

route_blog = Blueprint('route_blog', __name__)

@route_blog.route('/blog', methods=['GET', 'POST'])
def blog():
    # Chiamata alla funzione
    me = BluLupo()
    articles_and_authors = get_articles_and_authors_raw()

    # Paginazione
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 3  # Numero di articoli per pagina
    total = len(articles_and_authors)
    # Calcola l'offset per recuperare gli articoli corretti
    offset = (page - 1) * per_page
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    # Estrai gli articoli per la pagina corrente
    articles_for_page = articles_and_authors[offset: offset + per_page]
    print(articles_for_page)

    return render_template('blog.html', articles=articles_for_page, pagination=pagination,me=me)
