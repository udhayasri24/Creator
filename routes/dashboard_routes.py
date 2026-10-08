"""
Dashboard routes for CreatorIQ — Milestone 3.
Renders the main analytics dashboard with real database-driven KPIs, charts, and platform summaries.
"""

from flask import Blueprint, render_template, session, request
from sqlalchemy.exc import SQLAlchemyError
from utils.auth import login_required
from utils import analytics_service as svc

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard_view():
    """
    Render the CreatorIQ Analytics Dashboard.
    Reads KPIs, top content, and platform summary from the Content table.
    All data is scoped to the current session user — never leaks across accounts.
    """
    user_id = session.get("user_id")

    # Parse date filter period from query string (default: last 30 days)
    period = request.args.get("period", "30")
    days = svc._parse_days(period)

    try:
        kpi_data = svc.get_kpi_summary(user_id, days)
        top_content = svc.get_top_content(user_id, limit=5, days=days)
        platform_data = svc.get_platform_performance(user_id, days)
    except SQLAlchemyError:
        # Gracefully degrade — show empty state
        kpi_data = {"has_data": False}
        top_content = []
        platform_data = {"platforms": []}

    # Platform connection info (Milestone 4 will link real connected accounts)
    platforms_ui = [
        {
            "id": "youtube",
            "name": "YouTube",
            "handle": "@creator_iq",
            "status": "Demo Data",
            "accent": "#FF0000",
            "desc": "Video performance, subscribers, and watch-time analytics"
        },
        {
            "id": "instagram",
            "name": "Instagram",
            "handle": "@creatoriq_hub",
            "status": "Demo Data",
            "accent": "#E1306C",
            "desc": "Reels reach, audience demographics, and story engagement"
        },
        {
            "id": "linkedin",
            "name": "LinkedIn",
            "handle": "in/creatoriq",
            "status": "Demo Data",
            "accent": "#0A66C2",
            "desc": "Professional content impressions, follower growth & industry reach"
        },
    ]

    return render_template(
        "dashboard.html",
        kpi_data=kpi_data,
        top_content=top_content,
        platform_data=platform_data,
        platforms=platforms_ui,
        period=period,
        active_page="dashboard",
        format_number=svc.format_number,
    )
