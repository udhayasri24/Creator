"""
Content Model for CreatorIQ — Milestone 3.
Stores analytics data for creator content across YouTube, Instagram, and LinkedIn.
Each record belongs to a single user and represents one piece of content.

NOTE: These records are currently populated via seed_demo_data.py (development only).
      In Milestone 4, they will also be populated by real social platform API sync.
"""

from datetime import datetime, timezone
from database import db


# Allowed platform and content-type values (enforced at model level)
VALID_PLATFORMS = ["YouTube", "Instagram", "LinkedIn"]
VALID_CONTENT_TYPES = ["Video", "Image", "Reel", "Short", "Post", "Article"]


class Content(db.Model):
    """
    Content analytics record for a single piece of creator content.

    Relationship:
        User (1) ──── (*) Content

    Security: user_id is always set server-side; never trust client-provided user_id.
    """

    __tablename__ = "content"

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Ownership — foreign key to users table
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Content identity
    platform = db.Column(db.String(50), nullable=False)          # YouTube | Instagram | LinkedIn
    title = db.Column(db.String(300), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)       # Video | Image | Reel | Short | Post | Article
    published_at = db.Column(db.DateTime, nullable=False)

    # Engagement metrics
    views = db.Column(db.BigInteger, default=0, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    comments = db.Column(db.Integer, default=0, nullable=False)
    shares = db.Column(db.Integer, default=0, nullable=False)
    saves = db.Column(db.Integer, default=0, nullable=False)

    # Reach / audience metrics
    reach = db.Column(db.BigInteger, default=0, nullable=False)
    impressions = db.Column(db.BigInteger, default=0, nullable=False)

    # Video-specific
    watch_time = db.Column(db.Integer, default=0, nullable=False)  # minutes

    # Pre-calculated engagement rate (stored for indexing / performance)
    # Recalculated and stored when content is created or updated.
    engagement_rate = db.Column(db.Float, default=0.0, nullable=False)

    # Record timestamps
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship to User model
    user = db.relationship("User", backref=db.backref("content_items", lazy="dynamic"))

    def __init__(self, user_id, platform, title, content_type, published_at,
                 views=0, likes=0, comments=0, shares=0, saves=0,
                 reach=0, impressions=0, watch_time=0):
        self.user_id = user_id
        self.platform = platform if platform in VALID_PLATFORMS else "YouTube"
        self.title = title.strip()
        self.content_type = content_type if content_type in VALID_CONTENT_TYPES else "Video"
        self.published_at = published_at
        self.views = max(0, int(views))
        self.likes = max(0, int(likes))
        self.comments = max(0, int(comments))
        self.shares = max(0, int(shares))
        self.saves = max(0, int(saves))
        self.reach = max(0, int(reach))
        self.impressions = max(0, int(impressions))
        self.watch_time = max(0, int(watch_time))
        self.engagement_rate = self._calculate_engagement_rate()

    def _calculate_engagement_rate(self):
        """
        Calculate engagement rate as a percentage.

        Formula: (likes + comments + shares + saves) / reach * 100
        Falls back to impressions if reach is 0.
        Returns 0.0 if neither reach nor impressions are available.
        """
        total_engagements = self.likes + self.comments + self.shares + self.saves
        denominator = self.reach if self.reach > 0 else self.impressions
        if denominator > 0:
            return round((total_engagements / denominator) * 100, 2)
        return 0.0

    def recalculate_engagement_rate(self):
        """Recalculate and store the engagement rate. Call before db.session.commit()."""
        self.engagement_rate = self._calculate_engagement_rate()

    def to_dict(self):
        """Serialize content record to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "platform": self.platform,
            "title": self.title,
            "content_type": self.content_type,
            "published_at": self.published_at.strftime("%Y-%m-%d") if self.published_at else None,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "shares": self.shares,
            "saves": self.saves,
            "reach": self.reach,
            "impressions": self.impressions,
            "watch_time": self.watch_time,
            "engagement_rate": self.engagement_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Content id={self.id} platform='{self.platform}' title='{self.title[:30]}...'>"
