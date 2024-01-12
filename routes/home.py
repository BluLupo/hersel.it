#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template, make_response
from utilities.aboutclass import BluLupo

route_home = Blueprint('route_home', __name__)

@route_home.route('/', methods=['GET', 'POST'])
@route_home.route('/home', methods=['GET', 'POST'])
@route_home.route('/index.php', methods=['GET', 'POST'])
def home():
    me = BluLupo()
    response = make_response(render_template('home.html',me=me))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response