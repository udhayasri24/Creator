"""
Authentication routes for CreatorIQ.
Provides UI views for Login and Registration (Milestone 1 UI Shell).
Full authentication logic, session handling, and password hashing will be implemented in Milestone 2.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Render Login UI page.
    In Milestone 1, form submission displays a demo message and provides
    an option to enter the demo dashboard.
    """
    if request.method == "POST":
        email = request.form.get("email")
        # In Milestone 1: UI Shell demo response
        flash(f"Welcome back! Demo login recognized for {email}. Redirecting to dashboard...", "info")
        return redirect(url_for("dashboard.dashboard_view"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Render Registration UI page.
    Accepts Full Name, Email, Password, Confirm Password, and Role.
    In Milestone 1, form submission displays a demo message and provides
    an option to enter the demo dashboard.
    """
    if request.method == "POST":
        full_name = request.form.get("full_name")
        role = request.form.get("role", "Creator")
        flash(f"Account created for {full_name} ({role})! Demo access granted.", "success")
        return redirect(url_for("dashboard.dashboard_view"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    """UI placeholder for user logout."""
    flash("You have been signed out from the demo session.", "info")
    return redirect(url_for("main.index"))
