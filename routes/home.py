#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Blueprint, render_template
from utilities.aboutclass import BluLupo

route_home = Blueprint('route_home', __name__)

@route_home.route('/', methods=['GET', 'POST'])
def home():
    me = BluLupo()
    return render_template('home.html',me=me)