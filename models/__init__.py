"""
Data Models Package for CreatorIQ.
Initializes and exposes SQLAlchemy model classes.
"""

from datetime import datetime, timezone
from database import db
from models.user import User


class PlatformAccount(db.Model):
    """
    Connected platform account model placeholder for Milestone 3+ integrations.
    Supports YouTube, Instagram, and LinkedIn.
    """
    __tablename__ = "platform_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    platform_name = db.Column(db.String(50), nullable=False)  # YouTube, Instagram, LinkedIn
    account_identifier = db.Column(db.String(150), nullable=True)
    is_connected = db.Column(db.Boolean, default=False)
    connected_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<PlatformAccount {self.platform_name} (Connected={self.is_connected})>"


__all__ = ["User", "PlatformAccount"]
