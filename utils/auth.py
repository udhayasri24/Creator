"""
Authentication Utilities for CreatorIQ.
Provides login verification decorators and session helper routines.
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, make_response


def login_required(f):
    """
    Decorator to protect routes requiring an active user session.
    Redirects unauthenticated visitors to the login page with an informative message.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))

        response = f(*args, **kwargs)
        # Ensure HTTP response prevents caching on protected routes
        resp = make_response(response)
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp

    return decorated_function


def get_current_user_data():
    """
    Helper function to retrieve authenticated user information from the session.
    Returns a dictionary or None if unauthenticated.
    """
    if not session.get("user_id"):
        return None

    full_name = session.get("user_name", "Creator")
    parts = full_name.strip().split()
    if len(parts) >= 2:
        initials = f"{parts[0][0]}{parts[1][0]}".upper()
    elif parts and len(parts[0]) > 0:
        initials = parts[0][:2].upper()
    else:
        initials = "CR"

    return {
        "id": session.get("user_id"),
        "name": full_name,
        "email": session.get("user_email", ""),
        "role": session.get("user_role", "Creator"),
        "initials": initials,
    }
