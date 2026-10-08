"""
Analytics API Routes for CreatorIQ — Milestone 3.
Provides JSON REST endpoints that power the dashboard charts and content analytics page.

All routes require authentication. All queries are scoped to the current session user_id.
A logged-in user can NEVER retrieve another user's data by manipulating URL parameters.

Endpoints:
    GET /api/analytics/summary          — KPI totals
    GET /api/analytics/trends           — Views by date (line chart)
    GET /api/analytics/engagement       — Likes / Comments / Shares / Saves breakdown
    GET /api/analytics/platforms        — Per-platform performance
    GET /api/analytics/top-content      — Top 5 content items
    GET /api/analytics/reach-engagement — Reach vs engagement scatter data
    GET /api/content                    — Full content table (with filters)

Query parameters (optional on all endpoints):
    period: "7" | "30" | "90" | "all"  (default: "30")
    platform: "YouTube" | "Instagram" | "LinkedIn"  (content endpoint only)
    content_type: "Video" | "Reel" | ...            (content endpoint only)
    search: str                                      (content endpoint only)
    sort_by: "views" | "engagement" | "published_at" (content endpoint only)
"""

from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError
from utils.auth import login_required
from utils import analytics_service as svc

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_user_id() -> int:
    """Return the current session user_id. Always use this — never trust client-sent user_id."""
    return session.get("user_id")


def _get_days():
    """Parse the 'period' query param and return integer days or None."""
    period = request.args.get("period", "30")
    return svc._parse_days(period)


# ---------------------------------------------------------------------------
# GET /api/analytics/summary
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/summary")
@login_required
def analytics_summary():
    """Return KPI totals for the authenticated user."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_kpi_summary(user_id, days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/analytics/trends
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/trends")
@login_required
def analytics_trends():
    """Return views grouped by date for the line chart."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_views_trend(user_id, days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/analytics/engagement
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/engagement")
@login_required
def analytics_engagement():
    """Return aggregated engagement breakdown (likes/comments/shares/saves)."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_engagement_overview(user_id, days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/analytics/platforms
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/platforms")
@login_required
def analytics_platforms():
    """Return per-platform performance metrics."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_platform_performance(user_id, days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/analytics/top-content
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/top-content")
@login_required
def analytics_top_content():
    """Return the top 5 content items ranked by engagement rate then views."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_top_content(user_id, limit=5, days=days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/analytics/reach-engagement
# ---------------------------------------------------------------------------

@api_bp.route("/analytics/reach-engagement")
@login_required
def analytics_reach_engagement():
    """Return reach vs engagement scatter data."""
    try:
        user_id = _get_user_id()
        days = _get_days()
        data = svc.get_reach_vs_engagement(user_id, days)
        return jsonify({"ok": True, "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500


# ---------------------------------------------------------------------------
# GET /api/content
# ---------------------------------------------------------------------------

@api_bp.route("/content")
@login_required
def content_list():
    """
    Return content records for the authenticated user with optional filters.

    Query params:
        period      — "7" | "30" | "90" | "all"
        platform    — "YouTube" | "Instagram" | "LinkedIn"
        content_type— "Video" | "Reel" | "Short" | "Image" | "Post" | "Article"
        search      — title substring
        sort_by     — "views" | "engagement" | "likes" | "published_at"
    """
    try:
        user_id = _get_user_id()
        days = _get_days()
        platform = request.args.get("platform", "").strip() or None
        content_type = request.args.get("content_type", "").strip() or None
        search = request.args.get("search", "").strip() or None
        sort_by = request.args.get("sort_by", "published_at")

        data = svc.get_content_list(
            user_id=user_id,
            platform=platform,
            content_type=content_type,
            search=search,
            sort_by=sort_by,
            days=days,
        )
        return jsonify({"ok": True, "count": len(data), "data": data})
    except SQLAlchemyError as e:
        return jsonify({"ok": False, "error": "Database error.", "detail": str(e)}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": "Unexpected error.", "detail": str(e)}), 500
