"""
Authentication routes for CreatorIQ.
Implements real user registration, login, and session logout backed by MySQL.
"""

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle new user registration.
    Validates form inputs, enforces unique email, hashes password,
    and inserts user into the MySQL database.
    """
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "Creator").strip()

        # 1. Validate required fields
        if not full_name or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)

        # 2. Validate email format
        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)

        # 3. Validate passwords match
        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)

        # 4. Check if email already exists in MySQL
        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("An account with this email already exists. Please log in.", "danger")
                return render_template("register.html", full_name=full_name, email=email, role=role)

            # 5. Create new user with hashed password
            new_user = User(
                full_name=full_name,
                email=email,
                password=password,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

        except OperationalError as err:
            db.session.rollback()
            flash("Database connection error. Please ensure MySQL is running and configured in .env.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)
        except IntegrityError as err:
            db.session.rollback()
            flash("An account with this email already exists.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)
        except SQLAlchemyError as err:
            db.session.rollback()
            flash("An unexpected database error occurred during registration. Please try again.", "danger")
            return render_template("register.html", full_name=full_name, email=email, role=role)

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user authentication.
    Queries MySQL for user by email and verifies password hash.
    Sets session upon successful credentials check.
    """
    # If already logged in, redirect straight to dashboard
    if session.get("user_id"):
        return redirect(url_for("dashboard.dashboard_view"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        next_url = request.args.get("next") or request.form.get("next")

        # Validate presence of credentials
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html", email=email)

        try:
            user = User.query.filter_by(email=email).first()

            # Enforce security: do not differentiate between non-existent email vs wrong password
            if not user or not user.check_password(password):
                flash("Invalid email or password.", "danger")
                return render_template("login.html", email=email)

            # Establish authenticated session
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["user_email"] = user.email
            session["user_role"] = user.role

            flash(f"Welcome back, {user.full_name}!", "success")

            # Validate redirect URL if present
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("dashboard.dashboard_view"))

        except OperationalError as err:
            flash("Database connection error. Please ensure MySQL is running and configured in .env.", "danger")
            return render_template("login.html", email=email)
        except SQLAlchemyError as err:
            flash("A database error occurred during login. Please try again.", "danger")
            return render_template("login.html", email=email)

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    Clear session and sign out the current user.
    Redirects to the login page.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
