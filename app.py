"""
CreatorIQ - Creator Analytics & Content Performance Dashboard
Main Application Entry Point (Milestone 2: Authentication & User Management)
"""

import os
from flask import Flask, render_template
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from config import config_by_name, Config
from database import db
from models import User, Content, PlatformAccount
from routes import register_routes
from utils.auth import get_current_user_data


def create_app(config_name=None, test_config=None):
    """
    Application factory pattern to configure and return the Flask application.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development").lower()

    app = Flask(__name__)
    selected_config = config_by_name.get(config_name, Config)
    app.config.from_object(selected_config)

    if test_config:
        app.config.update(test_config)

    # Diagnostic: print the DB URI (password masked) to confirm .env was loaded
    raw_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "NOT SET")
    masked_uri = raw_uri
    if "@" in raw_uri and ":" in raw_uri:
        try:
            scheme, rest = raw_uri.split("://", 1)
            userinfo, hostpart = rest.rsplit("@", 1)
            if ":" in userinfo:
                uname, _ = userinfo.split(":", 1)
                masked_uri = f"{scheme}://{uname}:***@{hostpart}"
        except Exception:
            masked_uri = "(could not mask)"
    print(f" [*] DB URI: {masked_uri}")

    # Initialize SQLAlchemy database instance
    db.init_app(app)

    # Automatically initialize MySQL tables if database is reachable
    with app.app_context():
        try:
            db.create_all()
            print(" [*] Database tables verified / created successfully.")
        except OperationalError as e:
            print(f" [!] MySQL Connection Notice: Could not connect to MySQL server ({e.args[0] if e.args else e}).")
            print(" [!] Please ensure MySQL is running and valid credentials are set in .env.")
        except SQLAlchemyError as e:
            print(f" [!] Database initialization error: {e}")

    # Inject authenticated user context across all templates
    @app.context_processor
    def inject_user():
        return dict(current_user=get_current_user_data())

    # Register modular route blueprints (Main, Auth, Dashboard, Analytics, Settings)
    register_routes(app)

    # Global error handling for clean user experience
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
    print(" [*] CreatorIQ Application is starting (Milestone 2 Auth & Management)")
    print(f" [*] Local URL: http://127.0.0.1:{port}")
    print(" [*] Authentication: Real MySQL User Management Active")
    print(" [*] Dark Mode / Light Mode ready")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=port, debug=debug)
