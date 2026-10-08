"""
Milestone 3 Automated Test Suite for CreatorIQ.

Tests:
    1.  Authenticated user can access /api/analytics/summary
    2.  Unauthenticated user cannot access analytics API (redirects to login)
    3.  Empty analytics summary returns zeros and has_data=False
    4.  Content records can be created and retrieved via API
    5.  KPI summary calculations are mathematically correct
    6.  Top content ranking works (sorted by engagement_rate then views)
    7.  Platform summary aggregates per-platform correctly
    8.  User isolation: User A cannot access User B's data
    9.  Date filter (period=7) restricts to recent records only
    10. Existing Milestone 2 authentication tests still pass

All tests use SQLite in-memory database (testing config) for full isolation.
"""

import unittest
from datetime import datetime, timedelta, timezone
from app import create_app
from database import db
from models.user import User
from models.content import Content


def _reg(client, email, name="Test User", password="TestPassword123!", role="Creator"):
    """Helper: register a user."""
    return client.post("/register", data={
        "full_name": name,
        "email": email,
        "password": password,
        "confirm_password": password,
        "role": role,
    })


def _login(client, email, password="TestPassword123!"):
    """Helper: log in a user."""
    return client.post("/login", data={"email": email, "password": password})


def _make_content(user_id, platform="YouTube", days_ago=5,
                  views=10000, likes=500, comments=100, shares=80, saves=60,
                  reach=15000, impressions=20000, title="Test Video",
                  content_type="Video"):
    """Helper: create a Content record with sensible defaults."""
    pub = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return Content(
        user_id=user_id,
        platform=platform,
        title=title,
        content_type=content_type,
        published_at=pub,
        views=views,
        likes=likes,
        comments=comments,
        shares=shares,
        saves=saves,
        reach=reach,
        impressions=impressions,
        watch_time=120,
    )


class Milestone3TestSuite(unittest.TestCase):
    """Automated tests for Milestone 3 — Analytics & Content Dashboard."""

    def setUp(self):
        """Set up test app with in-memory SQLite database."""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # -------------------------------------------------------------------------
    # 1. Authenticated user can access analytics API
    # -------------------------------------------------------------------------
    def test_01_authenticated_user_can_access_summary_api(self):
        """Authenticated user receives 200 JSON from /api/analytics/summary."""
        _reg(self.client, "user1@test.com")
        _login(self.client, "user1@test.com")

        resp = self.client.get("/api/analytics/summary")
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertIn("data", data)
        self.assertIn("total_views", data["data"])
        self.assertIn("avg_engagement_rate", data["data"])
        self.assertIn("has_data", data["data"])

    # -------------------------------------------------------------------------
    # 2. Unauthenticated user cannot access analytics API
    # -------------------------------------------------------------------------
    def test_02_unauthenticated_user_blocked_from_api(self):
        """Unauthenticated requests to all API endpoints redirect to login (302)."""
        api_routes = [
            "/api/analytics/summary",
            "/api/analytics/trends",
            "/api/analytics/engagement",
            "/api/analytics/platforms",
            "/api/analytics/top-content",
            "/api/analytics/reach-engagement",
            "/api/content",
        ]
        for route in api_routes:
            resp = self.client.get(route, follow_redirects=False)
            self.assertIn(
                resp.status_code, [302, 401],
                f"Route {route} should require auth. Got {resp.status_code}"
            )

    # -------------------------------------------------------------------------
    # 3. Empty analytics returns zeros and has_data=False
    # -------------------------------------------------------------------------
    def test_03_empty_analytics_returns_zeros(self):
        """User with no content gets has_data=False and zero KPI values."""
        _reg(self.client, "empty@test.com")
        _login(self.client, "empty@test.com")

        resp = self.client.get("/api/analytics/summary")
        data = resp.get_json()["data"]
        self.assertFalse(data["has_data"])
        self.assertEqual(data["total_views"], 0)
        self.assertEqual(data["total_likes"], 0)
        self.assertEqual(data["total_content"], 0)
        self.assertEqual(data["avg_engagement_rate"], 0.0)

    # -------------------------------------------------------------------------
    # 4. Content records can be created and retrieved
    # -------------------------------------------------------------------------
    def test_04_content_records_can_be_retrieved(self):
        """Content records created in DB appear in /api/content response."""
        _reg(self.client, "creator@test.com")
        _login(self.client, "creator@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="creator@test.com").first()
            c1 = _make_content(user.id, title="Video Alpha")
            c2 = _make_content(user.id, title="Video Beta", platform="Instagram",
                               content_type="Reel")
            db.session.add_all([c1, c2])
            db.session.commit()

        resp = self.client.get("/api/content?period=all")
        json_data = resp.get_json()
        self.assertTrue(json_data["ok"])
        self.assertEqual(json_data["count"], 2)
        titles = [item["title"] for item in json_data["data"]]
        self.assertIn("Video Alpha", titles)
        self.assertIn("Video Beta", titles)

    # -------------------------------------------------------------------------
    # 5. KPI calculations are correct
    # -------------------------------------------------------------------------
    def test_05_kpi_calculations_are_correct(self):
        """
        KPI summary correctly sums views, likes, comments, shares, reach
        and calculates engagement rate = (likes+comments+shares+saves)/reach*100.
        """
        _reg(self.client, "kpi@test.com")
        _login(self.client, "kpi@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="kpi@test.com").first()
            # Two records with known values
            c1 = _make_content(user.id, views=10000, likes=200, comments=50,
                               shares=30, saves=20, reach=5000)
            c2 = _make_content(user.id, views=5000, likes=100, comments=25,
                               shares=15, saves=10, reach=2500)
            db.session.add_all([c1, c2])
            db.session.commit()

        resp = self.client.get("/api/analytics/summary?period=all")
        data = resp.get_json()["data"]

        self.assertEqual(data["total_views"], 15000)
        self.assertEqual(data["total_likes"], 300)
        self.assertEqual(data["total_comments"], 75)
        self.assertEqual(data["total_shares"], 45)
        self.assertEqual(data["total_reach"], 7500)
        self.assertEqual(data["total_content"], 2)
        self.assertTrue(data["has_data"])

        # Engagement rate: (300+75+45+30) / 7500 * 100 = 6.0%
        expected_eng = round((300 + 75 + 45 + 30) / 7500 * 100, 2)
        self.assertAlmostEqual(data["avg_engagement_rate"], expected_eng, places=1)

    # -------------------------------------------------------------------------
    # 6. Top content ranking is correct
    # -------------------------------------------------------------------------
    def test_06_top_content_ranked_by_engagement(self):
        """Top content is returned sorted by engagement_rate descending."""
        _reg(self.client, "top@test.com")
        _login(self.client, "top@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="top@test.com").first()
            # High engagement content
            c_high = _make_content(user.id, title="High Eng Video",
                                   likes=1000, comments=200, shares=150, saves=100,
                                   reach=5000)
            # Low engagement content
            c_low = _make_content(user.id, title="Low Eng Video",
                                  likes=50, comments=10, shares=5, saves=5,
                                  reach=10000)
            db.session.add_all([c_high, c_low])
            db.session.commit()

        resp = self.client.get("/api/analytics/top-content?period=all")
        data = resp.get_json()["data"]
        self.assertGreater(len(data), 0)
        # First result should be the high engagement one
        self.assertEqual(data[0]["title"], "High Eng Video")
        self.assertEqual(data[0]["rank"], 1)
        # Engagement rate of second should be lower
        if len(data) >= 2:
            self.assertGreaterEqual(data[0]["engagement_rate"], data[1]["engagement_rate"])

    # -------------------------------------------------------------------------
    # 7. Platform summary aggregates correctly
    # -------------------------------------------------------------------------
    def test_07_platform_summary_aggregates_correctly(self):
        """Platform endpoint returns entries for YouTube, Instagram, LinkedIn."""
        _reg(self.client, "plat@test.com")
        _login(self.client, "plat@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="plat@test.com").first()
            for platform in ["YouTube", "Instagram", "LinkedIn"]:
                c = _make_content(user.id, platform=platform,
                                  title=f"{platform} Test Content",
                                  content_type="Video" if platform == "YouTube" else "Post",
                                  views=1000, likes=100, comments=20, shares=15, saves=10,
                                  reach=2000)
                db.session.add(c)
            db.session.commit()

        resp = self.client.get("/api/analytics/platforms?period=all")
        data = resp.get_json()["data"]
        platforms_returned = {p["platform"] for p in data["platforms"]}
        self.assertIn("YouTube", platforms_returned)
        self.assertIn("Instagram", platforms_returned)
        self.assertIn("LinkedIn", platforms_returned)

        # Verify correct views for YouTube
        yt = next(p for p in data["platforms"] if p["platform"] == "YouTube")
        self.assertEqual(yt["total_views"], 1000)

    # -------------------------------------------------------------------------
    # 8. User isolation — User A cannot see User B's content
    # -------------------------------------------------------------------------
    def test_08_user_isolation_enforced(self):
        """User A's API calls only return User A's content, never User B's."""
        # Register both users
        _reg(self.client, "usera@test.com", name="User A")
        _reg(self.client, "userb@test.com", name="User B")

        # Create content for both users within a single app context
        with self.app.app_context():
            userA = User.query.filter_by(email="usera@test.com").first()
            userB = User.query.filter_by(email="userb@test.com").first()
            self.assertIsNotNone(userA, "User A should be registered")
            self.assertIsNotNone(userB, "User B should be registered")
            ca = _make_content(userA.id, title="User A Private Video", views=99999)
            cb = _make_content(userB.id, title="User B Private Video", views=55555)
            db.session.add_all([ca, cb])
            db.session.commit()

        # Log in as User A and check content list
        _login(self.client, "usera@test.com")
        resp = self.client.get("/api/content?period=all")
        json_data = resp.get_json()
        titles = [item["title"] for item in json_data["data"]]
        self.assertIn("User A Private Video", titles)
        self.assertNotIn("User B Private Video", titles)

        # Log in as User B and verify they only see their own content
        self.client.get("/logout")
        _login(self.client, "userb@test.com")
        resp2 = self.client.get("/api/content?period=all")
        json_data2 = resp2.get_json()
        titles2 = [item["title"] for item in json_data2["data"]]
        self.assertIn("User B Private Video", titles2)
        self.assertNotIn("User A Private Video", titles2)

    # -------------------------------------------------------------------------
    # 9. Date filter restricts results correctly
    # -------------------------------------------------------------------------
    def test_09_date_filter_restricts_by_period(self):
        """period=7 returns only content published in last 7 days."""
        _reg(self.client, "filter@test.com")
        _login(self.client, "filter@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="filter@test.com").first()
            # Recent: 3 days ago
            c_recent = _make_content(user.id, title="Recent Content", days_ago=3)
            # Old: 45 days ago
            c_old = _make_content(user.id, title="Old Content", days_ago=45)
            db.session.add_all([c_recent, c_old])
            db.session.commit()

        # With period=7, should only see recent content
        resp = self.client.get("/api/content?period=7")
        json_data = resp.get_json()
        titles = [item["title"] for item in json_data["data"]]
        self.assertIn("Recent Content", titles)
        self.assertNotIn("Old Content", titles)

        # With period=all, should see both
        resp_all = self.client.get("/api/content?period=all")
        json_all = resp_all.get_json()
        titles_all = [item["title"] for item in json_all["data"]]
        self.assertIn("Recent Content", titles_all)
        self.assertIn("Old Content", titles_all)

    # -------------------------------------------------------------------------
    # 10. Dashboard page is accessible and shows analytics content
    # -------------------------------------------------------------------------
    def test_10_dashboard_renders_after_content_added(self):
        """Dashboard returns 200 and shows analytics section when data exists."""
        _reg(self.client, "dash@test.com", name="Dash User")
        _login(self.client, "dash@test.com")

        # Empty state should render without error
        resp_empty = self.client.get("/dashboard")
        self.assertEqual(resp_empty.status_code, 200)
        self.assertIn(b"No Analytics Data Available Yet", resp_empty.data)

        # Add content
        with self.app.app_context():
            user = User.query.filter_by(email="dash@test.com").first()
            c = _make_content(user.id, title="My First Video", views=5000)
            db.session.add(c)
            db.session.commit()

        # Dashboard should now show KPI section
        resp_with_data = self.client.get("/dashboard")
        self.assertEqual(resp_with_data.status_code, 200)
        self.assertIn(b"Total Views", resp_with_data.data)

    # -------------------------------------------------------------------------
    # 11. Content analytics page filters work
    # -------------------------------------------------------------------------
    def test_11_content_analytics_platform_filter(self):
        """Platform filter on /content-analytics only shows matching platform content."""
        _reg(self.client, "filt2@test.com")
        _login(self.client, "filt2@test.com")

        with self.app.app_context():
            user = User.query.filter_by(email="filt2@test.com").first()
            yt = _make_content(user.id, platform="YouTube", title="YT Video")
            ig = _make_content(user.id, platform="Instagram",
                               title="IG Reel", content_type="Reel")
            db.session.add_all([yt, ig])
            db.session.commit()

        resp = self.client.get("/api/content?platform=YouTube&period=all")
        data = resp.get_json()
        platforms = {item["platform"] for item in data["data"]}
        self.assertEqual(platforms, {"YouTube"})

    # -------------------------------------------------------------------------
    # Existing Milestone 2 auth tests (regression)
    # -------------------------------------------------------------------------
    def test_12_m2_registration_still_works(self):
        """Milestone 2 regression: user registration still creates hashed password."""
        resp = self.client.post("/register", data={
            "full_name": "Regression User",
            "email": "regress@test.com",
            "password": "RegPassWord123!",
            "confirm_password": "RegPassWord123!",
            "role": "Creator"
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Registration successful. Please log in.", resp.data)
        with self.app.app_context():
            user = User.query.filter_by(email="regress@test.com").first()
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password("RegPassWord123!"))

    def test_13_m2_protected_routes_still_require_auth(self):
        """Milestone 2 regression: all protected routes still redirect unauthenticated users."""
        protected = ["/dashboard", "/content-analytics", "/audience-analytics",
                     "/growth-trends", "/revenue", "/platforms", "/reports",
                     "/notifications", "/settings"]
        for route in protected:
            resp = self.client.get(route, follow_redirects=False)
            self.assertEqual(resp.status_code, 302, f"{route} must redirect unauthenticated users")
            self.assertIn("/login", resp.headers["Location"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
