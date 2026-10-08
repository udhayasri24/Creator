"""
Analytics Service for CreatorIQ — Milestone 3.
Provides pure query and calculation functions for dashboard KPIs, charts, and content listings.

All functions accept a user_id parameter. Queries are always scoped to that user_id
to ensure strict data isolation between accounts.

NOTE: These functions query the Content table which is populated via seed_demo_data.py
      in development. Milestone 4 will add real API sync to this same table.
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from database import db
from models.content import Content


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def _get_cutoff_date(days: int | None) -> datetime | None:
    """Return a UTC datetime cutoff, or None for All Time."""
    if days is None:
        return None
    return datetime.now(timezone.utc) - timedelta(days=days)


def _parse_days(period: str) -> int | None:
    """Convert a human-readable period string to integer days, or None for All Time."""
    mapping = {"7": 7, "30": 30, "90": 90, "all": None}
    return mapping.get(str(period), None)


def _base_query(user_id: int, days: int | None):
    """Return a base Content query scoped to user_id, optionally date-filtered."""
    q = Content.query.filter_by(user_id=user_id)
    cutoff = _get_cutoff_date(days)
    if cutoff:
        q = q.filter(Content.published_at >= cutoff)
    return q


# ---------------------------------------------------------------------------
# KPI Summary
# ---------------------------------------------------------------------------

def get_kpi_summary(user_id: int, days: int | None = None) -> dict:
    """
    Calculate and return KPI metrics for the authenticated user.

    Returns a dict with total_views, total_likes, total_comments,
    total_shares, total_reach, avg_engagement_rate, and total_content.
    Returns zeroed dict if no content records exist.
    """
    q = _base_query(user_id, days)

    result = q.with_entities(
        func.coalesce(func.sum(Content.views), 0).label("total_views"),
        func.coalesce(func.sum(Content.likes), 0).label("total_likes"),
        func.coalesce(func.sum(Content.comments), 0).label("total_comments"),
        func.coalesce(func.sum(Content.shares), 0).label("total_shares"),
        func.coalesce(func.sum(Content.saves), 0).label("total_saves"),
        func.coalesce(func.sum(Content.reach), 0).label("total_reach"),
        func.count(Content.id).label("total_content"),
    ).one()

    total_views = int(result.total_views)
    total_likes = int(result.total_likes)
    total_comments = int(result.total_comments)
    total_shares = int(result.total_shares)
    total_saves = int(result.total_saves)
    total_reach = int(result.total_reach)
    total_content = int(result.total_content)

    # Engagement rate: (likes + comments + shares + saves) / reach * 100
    total_engagements = total_likes + total_comments + total_shares + total_saves
    avg_engagement_rate = round((total_engagements / total_reach) * 100, 2) if total_reach > 0 else 0.0

    return {
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_saves": total_saves,
        "total_reach": total_reach,
        "total_content": total_content,
        "avg_engagement_rate": avg_engagement_rate,
        "has_data": total_content > 0,
    }


# ---------------------------------------------------------------------------
# Views Trend (grouped by date)
# ---------------------------------------------------------------------------

def get_views_trend(user_id: int, days: int | None = 30) -> dict:
    """
    Return views grouped by published_at date for a line chart.
    Returns {"labels": [...dates...], "data": [...views...]}.
    """
    q = _base_query(user_id, days)

    rows = (
        q.with_entities(
            func.date(Content.published_at).label("pub_date"),
            func.sum(Content.views).label("daily_views"),
        )
        .group_by(func.date(Content.published_at))
        .order_by(func.date(Content.published_at))
        .all()
    )

    labels = [str(row.pub_date) for row in rows]
    data = [int(row.daily_views) for row in rows]
    return {"labels": labels, "data": data}


# ---------------------------------------------------------------------------
# Engagement Overview (Likes / Comments / Shares / Saves)
# ---------------------------------------------------------------------------

def get_engagement_overview(user_id: int, days: int | None = 30) -> dict:
    """
    Return aggregated engagement breakdown for a bar chart.
    Returns {"labels": [...metric names...], "data": [...totals...]}.
    """
    q = _base_query(user_id, days)

    result = q.with_entities(
        func.coalesce(func.sum(Content.likes), 0),
        func.coalesce(func.sum(Content.comments), 0),
        func.coalesce(func.sum(Content.shares), 0),
        func.coalesce(func.sum(Content.saves), 0),
    ).one()

    return {
        "labels": ["Likes", "Comments", "Shares", "Saves"],
        "data": [int(result[0]), int(result[1]), int(result[2]), int(result[3])],
    }


# ---------------------------------------------------------------------------
# Platform Performance
# ---------------------------------------------------------------------------

def get_platform_performance(user_id: int, days: int | None = None) -> dict:
    """
    Return per-platform aggregated metrics.
    Returns {"labels": [...platforms...], "views": [...], "engagement_rate": [...]}.
    """
    q = _base_query(user_id, days)

    rows = (
        q.with_entities(
            Content.platform,
            func.count(Content.id).label("content_count"),
            func.coalesce(func.sum(Content.views), 0).label("total_views"),
            func.coalesce(func.sum(Content.likes), 0).label("total_likes"),
            func.coalesce(func.sum(Content.comments), 0).label("total_comments"),
            func.coalesce(func.sum(Content.shares), 0).label("total_shares"),
            func.coalesce(func.sum(Content.saves), 0).label("total_saves"),
            func.coalesce(func.sum(Content.reach), 0).label("total_reach"),
        )
        .group_by(Content.platform)
        .order_by(Content.platform)
        .all()
    )

    platforms = []
    for row in rows:
        total_eng = int(row.total_likes) + int(row.total_comments) + int(row.total_shares) + int(row.total_saves)
        reach = int(row.total_reach)
        eng_rate = round((total_eng / reach) * 100, 2) if reach > 0 else 0.0

        platforms.append({
            "platform": row.platform,
            "content_count": int(row.content_count),
            "total_views": int(row.total_views),
            "total_likes": int(row.total_likes),
            "total_comments": int(row.total_comments),
            "total_shares": int(row.total_shares),
            "total_saves": int(row.total_saves),
            "total_reach": reach,
            "engagement_rate": eng_rate,
        })

    # Ensure all three platforms appear (even with zeros)
    present = {p["platform"] for p in platforms}
    for platform_name in ["YouTube", "Instagram", "LinkedIn"]:
        if platform_name not in present:
            platforms.append({
                "platform": platform_name,
                "content_count": 0,
                "total_views": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0,
                "total_saves": 0,
                "total_reach": 0,
                "engagement_rate": 0.0,
            })

    # Sort by defined order
    order = ["YouTube", "Instagram", "LinkedIn"]
    platforms.sort(key=lambda p: order.index(p["platform"]) if p["platform"] in order else 99)

    return {
        "platforms": platforms,
        "labels": [p["platform"] for p in platforms],
        "views_data": [p["total_views"] for p in platforms],
        "engagement_data": [p["engagement_rate"] for p in platforms],
    }


# ---------------------------------------------------------------------------
# Top Performing Content
# ---------------------------------------------------------------------------

def get_top_content(user_id: int, limit: int = 5, days: int | None = None) -> list:
    """
    Return the top-performing content ranked by engagement rate, then views.
    Each item is a dict with rank, title, platform, views, and engagement_rate.
    """
    q = _base_query(user_id, days)

    rows = (
        q.order_by(Content.engagement_rate.desc(), Content.views.desc())
        .limit(limit)
        .all()
    )

    results = []
    for rank, content in enumerate(rows, start=1):
        results.append({
            "rank": rank,
            "id": content.id,
            "title": content.title,
            "platform": content.platform,
            "content_type": content.content_type,
            "published_at": content.published_at.strftime("%Y-%m-%d") if content.published_at else None,
            "views": content.views,
            "likes": content.likes,
            "comments": content.comments,
            "shares": content.shares,
            "saves": content.saves,
            "reach": content.reach,
            "engagement_rate": content.engagement_rate,
        })
    return results


# ---------------------------------------------------------------------------
# Reach vs Engagement data
# ---------------------------------------------------------------------------

def get_reach_vs_engagement(user_id: int, days: int | None = 30) -> dict:
    """
    Return scatter-chart data comparing reach and engagement rate per content item.
    """
    q = _base_query(user_id, days)
    rows = q.order_by(Content.published_at.desc()).limit(30).all()

    return {
        "labels": [c.title[:40] for c in rows],
        "reach_data": [c.reach for c in rows],
        "engagement_data": [c.engagement_rate for c in rows],
    }


# ---------------------------------------------------------------------------
# Content listing (for /content-analytics table)
# ---------------------------------------------------------------------------

def get_content_list(user_id: int, platform: str | None = None,
                     content_type: str | None = None, search: str | None = None,
                     sort_by: str = "published_at", days: int | None = None) -> list:
    """
    Return all content records for a user with optional filters.
    Supports platform filter, content type filter, title search, and sort order.
    """
    q = _base_query(user_id, days)

    if platform and platform.strip():
        q = q.filter(Content.platform == platform.strip())
    if content_type and content_type.strip():
        q = q.filter(Content.content_type == content_type.strip())
    if search and search.strip():
        q = q.filter(Content.title.ilike(f"%{search.strip()}%"))

    # Sorting options
    sort_map = {
        "views": Content.views.desc(),
        "engagement": Content.engagement_rate.desc(),
        "likes": Content.likes.desc(),
        "published_at": Content.published_at.desc(),
    }
    order_col = sort_map.get(sort_by, Content.published_at.desc())
    q = q.order_by(order_col)

    return [c.to_dict() for c in q.all()]


# ---------------------------------------------------------------------------
# Formatting helpers (used by templates)
# ---------------------------------------------------------------------------

def format_number(n: int | float) -> str:
    """Format large numbers with K/M suffixes for compact display."""
    if n is None:
        return "0"
    n = float(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(int(n))
