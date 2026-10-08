"""
Routes initialization package.
Registers all application blueprints with the Flask app.
"""

from flask import Blueprint


def register_routes(app):
    """Register all modular route blueprints with the application."""
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
