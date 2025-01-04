#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from quart import Blueprint, render_template

route_home = Blueprint('route_home', __name__)

@route_home.route('/')
async def home():
    return await render_template('index.html')
