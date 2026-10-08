"""
CreatorIQ — Demo Data Seed Script (Development Only)
=====================================================

PURPOSE:
    Creates realistic sample content analytics records in MySQL for development
    and demonstration purposes.

    This script is COMPLETELY SEPARATE from the application startup.
    It does NOT run automatically when Flask starts.
    It MUST be run manually from the terminal.

USAGE:
    python seed_demo_data.py [--email user@example.com]

    If --email is not supplied, the script will use the first registered user
    in the database, or create a dedicated demo user (demo@creatoriq.dev).

IDEMPOTENT:
    The script checks for existing demo records before inserting.
    It will NOT create duplicate records if run multiple times.
    To force a reseed, run with --reset flag (deletes existing demo records first).

MILESTONE NOTE:
    These records simulate data that would normally come from YouTube, Instagram,
    and LinkedIn APIs. In Milestone 4, real API sync will populate this same
    Content table with authentic metrics. The seed records will then be replaced
    or supplemented by real platform data.

USAGE EXAMPLES:
    python seed_demo_data.py                         # seed for first user or demo user
    python seed_demo_data.py --email me@example.com # seed for specific user
    python seed_demo_data.py --reset                 # delete existing demo data and reseed
"""

import sys
import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add project root to path and load environment
sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env", override=True)

from app import create_app
from database import db
from models.user import User
from models.content import Content

# ============================================================================
# DEMO DATA CONFIGURATION
# Demo records are clearly labeled with this prefix so they can be identified.
# ============================================================================

DEMO_MARKER = "[DEMO]"
DEMO_EMAIL = "demo@creatoriq.dev"

# Realistic-looking demo content items
DEMO_CONTENT = [
    # YouTube Videos
    {
        "platform": "YouTube",
        "title": "Building a Full-Stack App with Flask and MySQL",
        "content_type": "Video",
        "days_ago": 3,
        "views": 42150, "likes": 3100, "comments": 284, "shares": 512, "saves": 890,
        "reach": 68000, "impressions": 85000, "watch_time": 18400,
    },
    {
        "platform": "YouTube",
        "title": "System Design Interview Masterclass 2026",
        "content_type": "Video",
        "days_ago": 8,
        "views": 33400, "likes": 2650, "comments": 215, "shares": 390, "saves": 720,
        "reach": 54000, "impressions": 72000, "watch_time": 15200,
    },
    {
        "platform": "YouTube",
        "title": "Python Tips Every Developer Should Know",
        "content_type": "Short",
        "days_ago": 14,
        "views": 28600, "likes": 2100, "comments": 145, "shares": 280, "saves": 540,
        "reach": 41000, "impressions": 58000, "watch_time": 4200,
    },
    {
        "platform": "YouTube",
        "title": "Top 10 VS Code Extensions for 2026",
        "content_type": "Video",
        "days_ago": 21,
        "views": 19800, "likes": 1450, "comments": 108, "shares": 195, "saves": 380,
        "reach": 32000, "impressions": 45000, "watch_time": 8600,
    },
    {
        "platform": "YouTube",
        "title": "Why Most Developers Fail at Code Reviews",
        "content_type": "Video",
        "days_ago": 35,
        "views": 15200, "likes": 1100, "comments": 92, "shares": 155, "saves": 290,
        "reach": 25000, "impressions": 36000, "watch_time": 6800,
    },
    {
        "platform": "YouTube",
        "title": "React vs Vue vs Svelte — 2026 Comparison",
        "content_type": "Video",
        "days_ago": 50,
        "views": 22400, "likes": 1680, "comments": 176, "shares": 248, "saves": 440,
        "reach": 36000, "impressions": 51000, "watch_time": 9800,
    },
    {
        "platform": "YouTube",
        "title": "Docker in 15 Minutes — Beginner Guide",
        "content_type": "Short",
        "days_ago": 65,
        "views": 31500, "likes": 2320, "comments": 198, "shares": 365, "saves": 610,
        "reach": 48000, "impressions": 65000, "watch_time": 5100,
    },
    {
        "platform": "YouTube",
        "title": "How I Built a SaaS in 30 Days",
        "content_type": "Video",
        "days_ago": 80,
        "views": 38700, "likes": 2850, "comments": 252, "shares": 420, "saves": 790,
        "reach": 62000, "impressions": 80000, "watch_time": 16200,
    },

    # Instagram Posts
    {
        "platform": "Instagram",
        "title": "Creator Monetization Strategy — Thread",
        "content_type": "Post",
        "days_ago": 2,
        "views": 26800, "likes": 4200, "comments": 382, "shares": 620, "saves": 1150,
        "reach": 38000, "impressions": 52000, "watch_time": 0,
    },
    {
        "platform": "Instagram",
        "title": "Top 10 Developer Tools 2026 — Carousel",
        "content_type": "Image",
        "days_ago": 7,
        "views": 19200, "likes": 3150, "comments": 274, "shares": 480, "saves": 860,
        "reach": 28000, "impressions": 41000, "watch_time": 0,
    },
    {
        "platform": "Instagram",
        "title": "My Morning Routine as a Full-Time Creator",
        "content_type": "Reel",
        "days_ago": 12,
        "views": 52400, "likes": 6800, "comments": 512, "shares": 940, "saves": 1680,
        "reach": 72000, "impressions": 95000, "watch_time": 8600,
    },
    {
        "platform": "Instagram",
        "title": "3 Mistakes New Developers Make (and how to fix them)",
        "content_type": "Reel",
        "days_ago": 18,
        "views": 44100, "likes": 5600, "comments": 421, "shares": 780, "saves": 1340,
        "reach": 61000, "impressions": 82000, "watch_time": 7200,
    },
    {
        "platform": "Instagram",
        "title": "Code Review Checklist — Save This!",
        "content_type": "Image",
        "days_ago": 28,
        "views": 15800, "likes": 2480, "comments": 188, "shares": 340, "saves": 720,
        "reach": 22000, "impressions": 34000, "watch_time": 0,
    },
    {
        "platform": "Instagram",
        "title": "How to Land Your First Developer Job in 2026",
        "content_type": "Reel",
        "days_ago": 42,
        "views": 38500, "likes": 4850, "comments": 365, "shares": 680, "saves": 1180,
        "reach": 53000, "impressions": 71000, "watch_time": 6400,
    },
    {
        "platform": "Instagram",
        "title": "Clean Code vs Fast Code — What Matters?",
        "content_type": "Post",
        "days_ago": 55,
        "views": 12600, "likes": 1980, "comments": 145, "shares": 265, "saves": 540,
        "reach": 18000, "impressions": 27000, "watch_time": 0,
    },
    {
        "platform": "Instagram",
        "title": "Behind the Scenes: My Recording Setup",
        "content_type": "Image",
        "days_ago": 70,
        "views": 9800, "likes": 1560, "comments": 112, "shares": 198, "saves": 380,
        "reach": 14000, "impressions": 21000, "watch_time": 0,
    },

    # LinkedIn Articles & Posts
    {
        "platform": "LinkedIn",
        "title": "How Creators Can Scale Their Monetization Strategy",
        "content_type": "Article",
        "days_ago": 5,
        "views": 26800, "likes": 2180, "comments": 312, "shares": 580, "saves": 890,
        "reach": 42000, "impressions": 58000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "The State of Developer Salaries in India 2026",
        "content_type": "Post",
        "days_ago": 11,
        "views": 38400, "likes": 3100, "comments": 448, "shares": 820, "saves": 1240,
        "reach": 61000, "impressions": 82000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "5 Lessons I Learned Growing to 100K Subscribers",
        "content_type": "Article",
        "days_ago": 19,
        "views": 21500, "likes": 1720, "comments": 246, "shares": 465, "saves": 720,
        "reach": 35000, "impressions": 48000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "Why I Switched from Software Engineering to Content Creation",
        "content_type": "Article",
        "days_ago": 30,
        "views": 31200, "likes": 2540, "comments": 365, "shares": 680, "saves": 1050,
        "reach": 50000, "impressions": 68000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "AI Tools That Actually Improved My Content Workflow",
        "content_type": "Post",
        "days_ago": 45,
        "views": 18600, "likes": 1480, "comments": 212, "shares": 398, "saves": 620,
        "reach": 30000, "impressions": 42000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "Content Calendar Template for Tech Creators [Free]",
        "content_type": "Post",
        "days_ago": 60,
        "views": 14200, "likes": 1140, "comments": 164, "shares": 305, "saves": 470,
        "reach": 23000, "impressions": 33000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "From 0 to 50K LinkedIn Followers: My Exact Strategy",
        "content_type": "Article",
        "days_ago": 75,
        "views": 42800, "likes": 3450, "comments": 498, "shares": 940, "saves": 1480,
        "reach": 68000, "impressions": 92000, "watch_time": 0,
    },
    {
        "platform": "LinkedIn",
        "title": "The Truth About Brand Deal Rates for Creators",
        "content_type": "Post",
        "days_ago": 85,
        "views": 29600, "likes": 2380, "comments": 340, "shares": 625, "saves": 980,
        "reach": 47000, "impressions": 64000, "watch_time": 0,
    },
]


def get_or_create_demo_user(app) -> User:
    """Fetch first registered user or create a demo user if none exists."""
    with app.app_context():
        user = User.query.first()
        if user:
            print(f"  [OK] Seeding for existing user: {user.email} (id={user.id})")
            return user

        # No users registered yet — create a demo account
        demo = User(
            full_name="Demo Creator",
            email=DEMO_EMAIL,
            password="DemoPassword2026!",
            role="Creator"
        )
        db.session.add(demo)
        db.session.commit()
        print(f"  [+] Created demo user: {DEMO_EMAIL} (password: DemoPassword2026!)")
        return demo


def count_existing_demo_records(app, user_id: int) -> int:
    """Count how many demo records already exist for this user."""
    with app.app_context():
        return Content.query.filter(
            Content.user_id == user_id,
            Content.title.like(f"%[DEMO]%")
        ).count()


def seed_content(app, user_id: int, reset: bool = False):
    """Insert demo content records. Idempotent — skips if records already exist."""
    with app.app_context():
        # Check existing demo records
        existing = Content.query.filter(
            Content.user_id == user_id,
            Content.title.like("%[DEMO]%")
        ).count()

        if existing > 0 and not reset:
            print(f"\n  [!] {existing} demo records already exist for user_id={user_id}.")
            print("      Run with --reset to delete and reseed.")
            return 0

        if reset and existing > 0:
            deleted = Content.query.filter(
                Content.user_id == user_id,
                Content.title.like("%[DEMO]%")
            ).delete()
            db.session.commit()
            print(f"  [OK] Deleted {deleted} existing demo records.")

        # Insert demo records
        now = datetime.now(timezone.utc)
        inserted = 0

        for item in DEMO_CONTENT:
            # Add a small random variation to make data more realistic
            jitter = random.uniform(0.88, 1.12)
            pub_date = now - timedelta(days=item["days_ago"])

            content = Content(
                user_id=user_id,
                platform=item["platform"],
                title=f"[DEMO] {item['title']}",     # clearly labelled as demo
                content_type=item["content_type"],
                published_at=pub_date,
                views=int(item["views"] * jitter),
                likes=int(item["likes"] * jitter),
                comments=int(item["comments"] * jitter),
                shares=int(item["shares"] * jitter),
                saves=int(item["saves"] * jitter),
                reach=int(item["reach"] * jitter),
                impressions=int(item["impressions"] * jitter),
                watch_time=int(item.get("watch_time", 0) * jitter),
            )
            db.session.add(content)
            inserted += 1

        db.session.commit()
        return inserted


def main():
    parser = argparse.ArgumentParser(
        description="CreatorIQ — Seed demo analytics data for development"
    )
    parser.add_argument(
        "--email",
        help="Email of the user to seed data for (default: first registered user)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing demo records and reseed"
    )
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  CreatorIQ — Demo Data Seed Script (Development Only)")
    print("=" * 60)
    print("  NOTE: These records are labelled [DEMO] and serve as")
    print("  stand-ins until Milestone 4 adds real API data.")
    print("=" * 60 + "\n")

    app = create_app()

    with app.app_context():
        db.create_all()

        # Resolve target user
        if args.email:
            user = User.query.filter_by(email=args.email.strip().lower()).first()
            if not user:
                print(f"  [!] No user found with email: {args.email}")
                print("      Register via /register first, then run this script.")
                sys.exit(1)
            print(f"  [OK] Seeding for user: {user.email} (id={user.id})")
        else:
            user = get_or_create_demo_user(app)

    # Seed data
    count = seed_content(app, user.id, reset=args.reset)

    if count > 0:
        print(f"\n  [OK] Inserted {count} demo content records for user_id={user.id}")
        print(f"\n  You can now log in and view the analytics dashboard.")
        print(f"  All records are labelled [DEMO] so you can easily identify them.")
        print(f"\n  To remove demo data, run: python seed_demo_data.py --reset")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
