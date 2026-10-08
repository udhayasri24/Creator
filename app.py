"""
CreatorIQ - Creator Analytics & Content Performance Dashboard
Main Application Entry Point (Milestone 1: Project Foundation & UI Shell)
"""

import os
from flask import Flask, render_template
from config import config_by_name, Config
from database import db
from routes import register_routes


def create_app(config_name=None):
    """
    Application factory pattern to configure and return the Flask application.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development").lower()

    app = Flask(__name__)
    selected_config = config_by_name.get(config_name, Config)
    app.config.from_object(selected_config)

    # Initialize SQLAlchemy database instance
    # Prepared for MySQL database connection in Milestone 2
    db.init_app(app)

    # Register modular route blueprints (Main, Auth, Dashboard)
    register_routes(app)

    # Error handling for clean user experience
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("base.html", error_title="404 - Page Not Found",
                               error_msg="The page you requested does not exist."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("base.html", error_title="500 - Server Error",
                               error_msg="An unexpected error occurred. Please try again later."), 500

    return app


# Instantiate app for WSGI and direct execution
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    print("\n" + "=" * 60)
    print(" [*] CreatorIQ Application is starting (Milestone 1 UI Shell)")
    print(f" [*] Local URL: http://127.0.0.1:{port}")
    print(" [*] Dark Mode / Light Mode ready")
    print(" [*] Sample Charts configured with Chart.js")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=port, debug=debug)
