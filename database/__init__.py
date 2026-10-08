"""
Database package for CreatorIQ.
Initializes the SQLAlchemy instance for application use.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
# Bound to the Flask app in app.py via db.init_app(app)
db = SQLAlchemy()
