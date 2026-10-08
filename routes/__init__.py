"""
Routes initialization package for CreatorIQ.
Registers all modular route blueprints with the Flask app.
"""


def register_routes(app):
    """Register all modular route blueprints with the application."""
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.analytics_routes import analytics_bp
    from routes.api_routes import api_bp
    from routes.settings_routes import settings_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(settings_bp)

