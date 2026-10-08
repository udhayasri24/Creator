"""
User Model for CreatorIQ.
Implements secure password hashing with Werkzeug and user profile attributes.
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    """
    User model representing registered creators, agencies, marketing teams, and administrators.
    Uses email as unique login identifier.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Creator")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    VALID_ROLES = ["Creator", "Agency", "Marketing Team", "Administrator"]

    def __init__(self, full_name, email, password, role="Creator"):
        self.full_name = full_name.strip()
        self.email = email.strip().lower()
        self.set_password(password)
        self.role = role if role in self.VALID_ROLES else "Creator"

    def set_password(self, password):
        """Hash and store the user's password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password against the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def get_initials(self):
        """Return 2-letter initials for user avatar display."""
        parts = self.full_name.strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts and len(parts[0]) > 0:
            return parts[0][:2].upper()
        return "CR"

    def to_dict(self):
        """Return user dictionary representation without password hash."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}' role='{self.role}'>"
