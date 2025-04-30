#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from quart import Quart, send_from_directory
from config import config
from routes.home import route_home

app = Quart(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# favicon.ico, sitemap.xml and robots.txt
@app.route('/favicon.ico')
async def favicon():
    return await send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/sitemap.xml')
async def sitemap():
    return await send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/robots.txt')
async def robots():
    return await send_from_directory(app.static_folder, 'robots.txt')

# BluePrint Routes
app.register_blueprint(route_home)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.APP_HOST, port=config.APP_PORT)
