"""
Dashboard routes for CreatorIQ.
Renders the CreatorIQ analytics dashboard shell, KPI summary cards,
platform connection cards, and sample chart visualizations.
"""

from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard_view():
    """
    Render the CreatorIQ Dashboard UI shell.
    Provides realistic Milestone 1 demo metrics and platform statuses.
    """
    # Demo KPI metrics for Milestone 1 UI presentation
    kpis = {
        "views": {"value": "125,430", "growth": "+14.2%", "period": "vs last month"},
        "likes": {"value": "18,240", "growth": "+8.5%", "period": "vs last month"},
        "followers": {"value": "42,850", "growth": "+5.1%", "period": "vs last month"},
        "engagement": {"value": "8.7%", "growth": "+1.8%", "period": "vs last month"},
        "revenue": {"value": "₹85,400", "growth": "+12.3%", "period": "vs last month"},
    }

    # Platform connection statuses (Milestone 1 shows 'Not Connected')
    platforms = [
        {
            "id": "youtube",
            "name": "YouTube",
            "handle": "@creator_iq",
            "status": "Not Connected",
            "accent": "#FF0000",
            "icon": "youtube",
            "desc": "Video performance, subscribers, and watch-time analytics"
        },
        {
            "id": "instagram",
            "name": "Instagram",
            "handle": "@creatoriq_hub",
            "status": "Not Connected",
            "accent": "#E1306C",
            "icon": "instagram",
            "desc": "Reels reach, audience demographics, and story engagement"
        },
        {
            "id": "linkedin",
            "name": "LinkedIn",
            "handle": "in/creatoriq",
            "status": "Not Connected",
            "accent": "#0A66C2",
            "icon": "linkedin",
            "desc": "Professional content impressions, follower growth & industry reach"
        }
    ]

    return render_template(
        "dashboard.html",
        kpis=kpis,
        platforms=platforms,
        user_name="Alex Rivera",
        user_role="Creator"
    )
