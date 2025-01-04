#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from quart import Quart
from config import config
from routes.home import route_home

app = Quart(__name__)

app.register_blueprint(route_home)

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.APP_HOST, port=config.APP_PORT)
