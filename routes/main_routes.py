"""
Main routes for CreatorIQ.
Handles the landing page and general marketing views.
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the CreatorIQ landing page."""
    return render_template("index.html")
