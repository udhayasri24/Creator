"""
Data Models Package for CreatorIQ.
Prepares SQLAlchemy model architectures for future milestones (Milestone 2+).
"""

from datetime import datetime
from database import db


class User(db.Model):
    """
    User model placeholder for Milestone 2 Authentication.
    Prepared schema for Creators, Agencies, Marketing Teams, and Administrators.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), default="Creator")  # Creator, Agency, Marketing Team, Administrator
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


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
