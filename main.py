#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

import os
from datetime import timedelta
from flask import Flask, send_from_directory, request, render_template
from routes.home import route_home
from routes.login import route_login
from routes.register import route_register
from routes.dashboard import route_dashboard
from routes.logout import route_logout
from routes.blog import route_blog
from routes.article import route_article
from routes.profile import route_profile
from routes.post_operations import route_changeusername
from config import Config
from database.connection import Database
from database.methods.website import create_data_website_options

app = Flask(__name__,template_folder="templates",static_folder="static",static_url_path='/static')
# Imposta la data di scadenza della sessione a 30 minuti
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

####################
## SERVICE ROUTES ##
####################
#Fake Route
@app.route('/wp-admin')
@app.route('/wp-content')
@app.route('/admin')
@app.route('/wp-login.php')
def wp():
  return "Ehhhh Volevi!"

#Route for Sitemap.xml and Robots.txt
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

#Load Favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html',message=error), 404

##############
### ROUTES ###
##############
app.register_blueprint(route_home)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_blog)
app.register_blueprint(route_article)
app.register_blueprint(route_profile)
app.register_blueprint(route_login)
app.register_blueprint(route_register)
app.register_blueprint(route_logout)
app.register_blueprint(route_changeusername)

if __name__ == '__main__':
    db = Database()
    db.create_tables_and_data()
    create_data_website_options()
    app.secret_key = Config.APP_SECRET
    app.run(debug=Config.APP_DEBUG,host=Config.APP_HOST,port=Config.APP_PORT)