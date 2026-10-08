"""
Milestone 2 Automated Test Suite for CreatorIQ.
Tests authentication, user registration, password hashing, route protection,
sidebar navigation endpoints, session persistence, and logout flow.
"""

import unittest
from app import create_app
from database import db
from models.user import User


class Milestone2TestSuite(unittest.TestCase):
    """Automated test cases for Milestone 2 features."""

    def setUp(self):
        """Set up test application with in-memory database context for isolated unit tests."""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_app_starts_and_home_route(self):
        """1 & 2: Verify application starts and landing page returns 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Creator Analytics", response.data)

    def test_02_login_and_register_pages_return_200(self):
        """3 & 4: Verify /login and /register return 200."""
        res_login = self.client.get("/login")
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Welcome Back", res_login.data)

        res_reg = self.client.get("/register")
        self.assertEqual(res_reg.status_code, 200)
        self.assertIn(b"Get Started with CreatorIQ", res_reg.data)

    def test_03_unauthenticated_dashboard_redirects_to_login(self):
        """5: Verify /dashboard redirects to /login when unauthenticated."""
        response = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

        # Following redirect shows the warning message
        res_followed = self.client.get("/dashboard", follow_redirects=True)
        self.assertEqual(res_followed.status_code, 200)
        self.assertIn(b"Please log in to continue.", res_followed.data)

    def test_04_all_sidebar_module_routes_exist_and_are_protected(self):
        """6 & 7: Verify all new module routes exist and redirect unauthenticated visitors."""
        protected_routes = [
            "/content-analytics",
            "/audience-analytics",
            "/growth-trends",
            "/revenue",
            "/platforms",
            "/reports",
            "/notifications",
            "/settings"
        ]
        for route in protected_routes:
            res = self.client.get(route, follow_redirects=False)
            self.assertEqual(res.status_code, 302, f"Route {route} should redirect when unauthenticated")
            self.assertIn("/login", res.headers["Location"])

    def test_05_user_registration_creates_database_user(self):
        """7: Verify registration creates user with hashed password."""
        res = self.client.post("/register", data={
            "full_name": "Test Creator",
            "email": "test@creatoriq.com",
            "password": "SecurePassword123!",
            "confirm_password": "SecurePassword123!",
            "role": "Creator"
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Registration successful. Please log in.", res.data)

        with self.app.app_context():
            user = User.query.filter_by(email="test@creatoriq.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.full_name, "Test Creator")
            self.assertEqual(user.role, "Creator")
            # Verify password was hashed (not plain text)
            self.assertNotEqual(user.password_hash, "SecurePassword123!")
            self.assertTrue(user.check_password("SecurePassword123!"))
            self.assertFalse(user.check_password("WrongPassword"))

    def test_06_duplicate_email_registration_rejected(self):
        """8: Verify duplicate registration with same email is rejected."""
        # Register first user
        self.client.post("/register", data={
            "full_name": "First User",
            "email": "duplicate@creatoriq.com",
            "password": "Password123",
            "confirm_password": "Password123",
            "role": "Creator"
        })

        # Attempt to register second user with same email
        res = self.client.post("/register", data={
            "full_name": "Second User",
            "email": "duplicate@creatoriq.com",
            "password": "Password123",
            "confirm_password": "Password123",
            "role": "Agency"
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"An account with this email already exists", res.data)

    def test_07_registration_validation_rules(self):
        """Validation: Missing fields, invalid email, password mismatch."""
        # Missing fields
        res_empty = self.client.post("/register", data={
            "full_name": "",
            "email": "",
            "password": "",
            "confirm_password": "",
            "role": "Creator"
        }, follow_redirects=True)
        self.assertIn(b"All fields are required.", res_empty.data)

        # Invalid email format
        res_invalid_email = self.client.post("/register", data={
            "full_name": "John Doe",
            "email": "not-an-email",
            "password": "Password123",
            "confirm_password": "Password123",
            "role": "Creator"
        }, follow_redirects=True)
        self.assertIn(b"Please enter a valid email address.", res_invalid_email.data)

        # Password mismatch
        res_mismatch = self.client.post("/register", data={
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "Password123",
            "confirm_password": "DifferentPassword",
            "role": "Creator"
        }, follow_redirects=True)
        self.assertIn(b"Password and Confirm Password do not match.", res_mismatch.data)

    def test_08_correct_credentials_login_and_access_dashboard(self):
        """9 & 12: Correct credentials successfully log in and access dashboard with real user data."""
        # 1. Register user
        self.client.post("/register", data={
            "full_name": "Sarah Connor",
            "email": "sarah@skynet.com",
            "password": "ValidPassword999",
            "confirm_password": "ValidPassword999",
            "role": "Marketing Team"
        })

        # 2. Login with correct credentials
        res_login = self.client.post("/login", data={
            "email": "sarah@skynet.com",
            "password": "ValidPassword999"
        }, follow_redirects=True)

        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Welcome back, Sarah Connor!", res_login.data)
        # Dashboard displays real user data and role
        self.assertIn(b"Sarah Connor", res_login.data)
        self.assertIn(b"Marketing Team", res_login.data)
        self.assertIn(b"SC", res_login.data)  # Initials

    def test_09_incorrect_password_and_nonexistent_email_rejected(self):
        """10 & 11: Verify wrong password and non-existent email are rejected."""
        # Register user
        self.client.post("/register", data={
            "full_name": "Valid User",
            "email": "valid@example.com",
            "password": "CorrectPassword",
            "confirm_password": "CorrectPassword",
            "role": "Creator"
        })

        # Attempt wrong password
        res_wrong_pw = self.client.post("/login", data={
            "email": "valid@example.com",
            "password": "WrongPassword"
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password.", res_wrong_pw.data)

        # Attempt non-existent email
        res_no_user = self.client.post("/login", data={
            "email": "nonexistent@example.com",
            "password": "AnyPassword"
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password.", res_no_user.data)

    def test_10_authenticated_user_can_access_all_module_pages(self):
        """13: Authenticated user can access all module pages with their sidebar."""
        # Register and login
        self.client.post("/register", data={
            "full_name": "David Miller",
            "email": "david@agency.com",
            "password": "SecretPassword",
            "confirm_password": "SecretPassword",
            "role": "Agency"
        })
        self.client.post("/login", data={
            "email": "david@agency.com",
            "password": "SecretPassword"
        })

        modules = [
            ("/content-analytics", b"Content Analytics"),
            ("/audience-analytics", b"Audience Analytics"),
            ("/growth-trends", b"Growth & Trends"),
            ("/revenue", b"Revenue Analytics"),
            ("/platforms", b"Platforms Management"),
            ("/reports", b"Reports & Exports"),
            ("/notifications", b"Notifications & Alerts"),
            ("/settings", b"Settings & Preferences"),
        ]

        for path, expected_text in modules:
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200, f"Failed on {path}")
            self.assertIn(expected_text, res.data)
            # Verify user info persists across all module pages
            self.assertIn(b"David Miller", res.data)
            self.assertIn(b"Agency", res.data)

    def test_11_logout_clears_session_and_protects_routes(self):
        """14 & 15: Logout clears authentication and protected pages redirect after logout."""
        # Register and login
        self.client.post("/register", data={
            "full_name": "Admin User",
            "email": "admin@creatoriq.com",
            "password": "AdminPassword123",
            "confirm_password": "AdminPassword123",
            "role": "Administrator"
        })
        self.client.post("/login", data={
            "email": "admin@creatoriq.com",
            "password": "AdminPassword123"
        })

        # Confirm access
        res_dash = self.client.get("/dashboard")
        self.assertEqual(res_dash.status_code, 200)

        # Logout
        res_logout = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn(b"You have been logged out.", res_logout.data)

        # Attempt to access dashboard again
        res_retry = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(res_retry.status_code, 302)
        self.assertIn("/login", res_retry.headers["Location"])

    def test_12_static_files_and_templates_valid(self):
        """16, 17, 18, 19: Verify static files and templates load properly without errors."""
        res_css = self.client.get("/static/css/style.css")
        self.assertEqual(res_css.status_code, 200)
        self.assertIn(b"CreatorIQ", res_css.data)

        res_js = self.client.get("/static/js/app.js")
        self.assertEqual(res_js.status_code, 200)
        self.assertIn(b"initThemeEngine", res_js.data)


if __name__ == "__main__":
    unittest.main()
