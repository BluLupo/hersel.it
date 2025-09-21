#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella
# Enhanced Quart Application with Database and Authentication

import asyncio
from quart import Quart, send_from_directory, session, g
from config import config
from models.database import init_database, db_manager
from utils.helpers import get_flash_messages
from utils.auth import get_current_user

# Import Blueprints
from routes.home import route_home
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app = Quart(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# Configuration
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

# Template globals
@app.template_global('get_flashed_messages')
def template_get_flashed_messages(with_categories=False):
    return get_flash_messages()

# Context processor for current user
@app.before_request
async def load_current_user():
    g.current_user = await get_current_user()

@app.context_processor
def inject_user():
    return {'current_user': getattr(g, 'current_user', None)}

# Static files routes
@app.route('/favicon.ico')
async def favicon():
    return await send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/sitemap.xml')
async def sitemap():
    return await send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/robots.txt')
async def robots():
    return await send_from_directory(app.static_folder, 'robots.txt')

# Register Blueprints
app.register_blueprint(route_home)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Database initialization
@app.before_serving
async def initialize_app():
    """Initialize database and other services"""
    print("🚀 Initializing Hersel.it application...")
    try:
        await init_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        # Don't crash the app, but log the error

@app.after_serving
async def cleanup_app():
    """Cleanup resources"""
    print("🔒 Shutting down Hersel.it application...")
    await db_manager.close_pool()
    print("✅ Application shutdown complete")

# Error handlers
@app.errorhandler(404)
async def not_found(error):
    return await render_template('errors/404.html'), 404

@app.errorhandler(500)
async def internal_error(error):
    return await render_template('errors/500.html'), 500

# Health check endpoint
@app.route('/health')
async def health_check():
    return {'status': 'healthy', 'app': 'Hersel.it Portfolio'}

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG, 
        host=config.APP_HOST, 
        port=config.APP_PORT
    )
