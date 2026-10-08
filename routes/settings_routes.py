"""
Settings routes for CreatorIQ.
Provides working /settings endpoint and placeholder view for account and application settings.
"""

from flask import Blueprint, render_template
from utils.auth import login_required

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings")
@login_required
def settings_view():
    """Render Settings placeholder view."""
    return render_template(
        "settings.html",
        active_page="settings",
        module_title="Settings & Preferences",
        module_description="Settings module will provide account and application settings."
    )
