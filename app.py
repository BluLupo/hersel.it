#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from flask import Flask, send_from_directory
from config import config
from models import db
from routes.home import route_home
from routes.api import route_api

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# Load configuration
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO

# Initialize database
db.init_app(app)

# favicon.ico, sitemap.xml and robots.txt
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

# BluePrint Routes
app.register_blueprint(route_home)
app.register_blueprint(route_api)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.APP_HOST, port=config.APP_PORT)
