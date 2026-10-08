"""
Analytics and module routes for CreatorIQ — Milestone 3.
Provides working endpoints for all sidebar navigation modules.

All routes are protected by @login_required.
Content analytics now serves real database data.
"""

from flask import Blueprint, render_template, request, session
from sqlalchemy.exc import SQLAlchemyError
from utils.auth import login_required
from utils import analytics_service as svc
from models.content import VALID_PLATFORMS, VALID_CONTENT_TYPES

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/content-analytics")
@login_required
def content_analytics():
    """
    Render the Content Analytics page with real database data.
    Supports search, platform filter, content type filter, and sort options.
    """
    user_id = session.get("user_id")

    # Read filter/sort params from query string
    period = request.args.get("period", "all")
    platform = request.args.get("platform", "").strip() or None
    content_type = request.args.get("content_type", "").strip() or None
    search = request.args.get("search", "").strip() or None
    sort_by = request.args.get("sort_by", "published_at")

    days = svc._parse_days(period)

    try:
        content_list = svc.get_content_list(
            user_id=user_id,
            platform=platform,
            content_type=content_type,
            search=search,
            sort_by=sort_by,
            days=days,
        )
        kpi_data = svc.get_kpi_summary(user_id, days)
    except SQLAlchemyError:
        content_list = []
        kpi_data = {"has_data": False}

    return render_template(
        "content_analytics.html",
        active_page="content_analytics",
        content_list=content_list,
        kpi_data=kpi_data,
        valid_platforms=VALID_PLATFORMS,
        valid_content_types=VALID_CONTENT_TYPES,
        period=period,
        selected_platform=platform or "",
        selected_type=content_type or "",
        search_query=search or "",
        sort_by=sort_by,
        format_number=svc.format_number,
    )


@analytics_bp.route("/audience-analytics")
@login_required
def audience_analytics():
    """Render Audience Analytics placeholder view (Milestone 4 will add real data)."""
    return render_template(
        "audience_analytics.html",
        active_page="audience_analytics",
        module_title="Audience Analytics",
        module_description="Audience Analytics will provide follower growth, demographics, audience behavior, reach, impressions, and active hours. Real data arrives in Milestone 4 via social platform APIs."
    )


@analytics_bp.route("/growth-trends")
@login_required
def growth_trends():
    """Render Growth & Trends placeholder view (Milestone 4 will add real data)."""
    return render_template(
        "growth_trends.html",
        active_page="growth_trends",
        module_title="Growth & Trends",
        module_description="Growth & Trends will provide growth monitoring, trend detection, hashtag analysis, and forecasting. Real data arrives in Milestone 4."
    )


@analytics_bp.route("/revenue")
@login_required
def revenue():
    """Render Revenue placeholder view (Milestone 5 will add real data)."""
    return render_template(
        "revenue.html",
        active_page="revenue",
        module_title="Revenue Analytics",
        module_description="Revenue will provide sponsorship, advertising, affiliate, brand collaboration, subscription, and earnings analytics. Coming in Milestone 5."
    )


@analytics_bp.route("/platforms")
@login_required
def platforms():
    """Render Platforms connection management view."""
    user_id = session.get("user_id")
    try:
        platform_data = svc.get_platform_performance(user_id, days=None)
    except SQLAlchemyError:
        platform_data = {"platforms": []}

    platforms_list = platform_data.get("platforms", [])
    return render_template(
        "platforms.html",
        active_page="platforms",
        platforms=platforms_list,
        module_title="Platforms Management",
        module_description="Platforms management will let you connect YouTube, Instagram, and LinkedIn accounts via OAuth in Milestone 4. Below is a summary of your current demo data."
    )


@analytics_bp.route("/reports")
@login_required
def reports():
    """Render Reports placeholder view."""
    return render_template(
        "reports.html",
        active_page="reports",
        module_title="Reports & Exports",
        module_description="Reports will provide analytics reports and export functionality in future milestones."
    )


@analytics_bp.route("/notifications")
@login_required
def notifications():
    """Render Notifications placeholder view."""
    return render_template(
        "notifications.html",
        active_page="notifications",
        module_title="Notifications & Alerts",
        module_description="Notifications will provide engagement, revenue, and reporting alerts in future milestones."
    )
