# CreatorIQ — Creator Analytics & Content Performance Dashboard

A centralized analytics platform where creators can monitor YouTube, Instagram, and LinkedIn channels to view content performance, audience analytics, growth trends, revenue analytics, reports, notifications, and platform comparisons from one unified command center.

---

## Current Milestone: Milestone 2 (Authentication & User Management)

> **Milestone Status:**  
> **Milestone 2** implements real user registration and login backed by MySQL using SQLAlchemy, secure password hashing with Werkzeug, session-based route protection (`@login_required`), dynamic user profile display, and working endpoints with placeholder pages for all 9 sidebar modules.
> 
> *Social media API integrations (YouTube, Instagram, LinkedIn OAuth), real analytics calculations, automated sync jobs, export engines, and cloud deployment are scheduled for subsequent milestones.*

---

## Technology Stack

### Frontend
- **HTML5**: Semantic document structuring
- **CSS3**: Vanilla CSS design system with CSS custom properties (variables) for instant Dark/Light mode switching
- **JavaScript**: Vanilla ES6+ for theme persistence (`localStorage`), mobile sidebar drawer, and chart updates
- **Chart.js (4.4)**: Interactive canvas visualizations for follower growth, views, engagement, and platform shares

### Backend
- **Python (3.13+)**: Application logic
- **Flask (3.1+)**: Clean, lightweight WSGI web framework using the Application Factory & Blueprints pattern
- **Werkzeug Security**: Cryptographic password hashing (`generate_password_hash`, `check_password_hash`)

### Database & ORM
- **MySQL**: Relational database engine
- **SQLAlchemy (via Flask-SQLAlchemy 3.1+)**: Object-Relational Mapping (ORM)
- **PyMySQL**: Pure-Python MySQL client driver
- **python-dotenv**: Environment configuration management

---

## Architecture Diagram

```
+-----------------------------------------------------------------+
|                        Client Browser                           |
|  - HTML5 / CSS3 / Vanilla JavaScript                            |
|  - Chart.js Visualizations (5 Interactive Canvas Charts)        |
|  - Theme Engine (Dark Mode / Light Mode with localStorage)      |
+-----------------------------------------------------------------+
                                |
                         HTTP / REST Requests
                                ↓
+-----------------------------------------------------------------+
|                       Flask Application                         |
|  - app.py (Application Factory: create_app)                     |
|  - utils/auth.py (@login_required decorator, session helpers)   |
|  - Blueprints:                                                  |
|      * main_bp      -> Landing Page (/)                         |
|      * auth_bp      -> Login, Register, Logout (/login, ...)    |
|      * dashboard_bp -> Main Dashboard (/dashboard)              |
|      * analytics_bp -> Content, Audience, Growth, Revenue, etc. |
|      * settings_bp  -> Settings & Preferences (/settings)       |
+-----------------------------------------------------------------+
                                |
                      Database Configuration
                                ↓
+-----------------------------------------------------------------+
|                   SQLAlchemy ORM Layer                          |
|  - config.py (DevelopmentConfig, TestingConfig, etc.)           |
|  - database/__init__.py (db instance)                           |
|  - models/user.py (User model with Werkzeug password hashing)   |
|  - models/__init__.py (User, PlatformAccount)                   |
+-----------------------------------------------------------------+
                                |
                         PyMySQL Connector
                                ↓
+-----------------------------------------------------------------+
|                         MySQL Database                          |
|  - users table (id, full_name, email, password_hash, role, ...) |
|  - platform_accounts table (prepared for Milestone 3)           |
+-----------------------------------------------------------------+
```

---

## Project Structure

```
creatoriq24/
│
├── app.py                  # Flask Application entry point & factory
├── config.py               # Environment & database configurations
├── requirements.txt        # Minimal required Python dependencies
├── .env.example            # Template for environment variables
├── .env                    # Local environment settings (git-ignored)
├── .gitignore              # Git ignore rules for Python, cache, and secrets
├── README.md               # Complete project documentation
│
├── database/               # Database initialization
│   └── __init__.py         # SQLAlchemy instance definition
│
├── models/                 # ORM Database Models
│   ├── __init__.py         # Model package exports
│   └── user.py             # User schema with Werkzeug password hashing
│
├── utils/                  # Application Utilities
│   └── auth.py             # @login_required decorator & session helpers
│
├── routes/                 # Modular Blueprint Routes
│   ├── __init__.py         # Blueprint registration logic
│   ├── main_routes.py      # Landing page route (/)
│   ├── auth_routes.py      # Registration, login & logout routes
│   ├── dashboard_routes.py # Dashboard UI shell route (/dashboard)
│   ├── analytics_routes.py # All sidebar analytics module routes
│   └── settings_routes.py  # User settings route (/settings)
│
├── templates/              # Jinja2 HTML Templates
│   ├── base.html           # Master layout with theme engine & Chart.js CDN
│   ├── dashboard_base.html # Unified layout with sidebar, topbar & user context
│   ├── index.html          # High-converting SaaS landing page
│   ├── login.html          # Real Login page
│   ├── register.html       # Real Register page (with creator roles)
│   ├── dashboard.html      # Main dashboard shell with KPI cards & charts
│   ├── content_analytics.html # Content Analytics placeholder module
│   ├── audience_analytics.html # Audience Analytics placeholder module
│   ├── growth_trends.html  # Growth & Trends placeholder module
│   ├── revenue.html        # Revenue Analytics placeholder module
│   ├── platforms.html      # Platform Management placeholder module
│   ├── reports.html        # Reports & Exports placeholder module
│   ├── notifications.html  # Notifications & Alerts placeholder module
│   └── settings.html       # Account Settings & Profile placeholder module
│
├── static/                 # Static Assets
│   ├── css/
│   │   └── style.css       # Unified design system, CSS variables & alerts
│   └── js/
│       └── app.js          # Dark/Light theme manager, sidebar toggle, Chart.js config
│
└── tests/                  # Automated Test Suite
    └── test_milestone2.py  # 12 automated test cases verifying Milestone 2
```

---

## Features Implemented in Milestone 2

1. **MySQL User Table with SQLAlchemy**:
   - `id`: Auto-incrementing primary key.
   - `full_name`: Creator's full name.
   - `email`: Unique login identifier.
   - `password_hash`: Cryptographically hashed using Werkzeug (`scrypt` / `pbkdf2`).
   - `role`: Supported roles: `Creator`, `Agency`, `Marketing Team`, `Administrator`.
   - `created_at`: UTC timestamp.

2. **Real User Registration (`/register`)**:
   - Form fields: Full Name, Email, Password, Confirm Password, Role.
   - Enforces field presence, regex email validation, password matching, and duplicate email prevention.
   - Hashes passwords securely; never stores plaintext passwords.
   - Displays clear error flash messages if validation fails.
   - Redirects to `/login` upon success with *"Registration successful. Please log in."*

3. **Real User Login (`/login`)**:
   - Form fields: Email, Password.
   - Queries database for user and validates password hash.
   - Rejects non-existent accounts and invalid passwords with uniform message: *"Invalid email or password."*
   - Sets secure Flask session (`user_id`, `user_name`, `user_email`, `user_role`).
   - Redirects to `/dashboard` upon successful login.

4. **Session-Based Authentication & Route Protection**:
   - `@login_required` decorator checks session presence.
   - Redirects unauthenticated visitors to `/login` with *"Please log in to continue."*
   - Adds HTTP headers to prevent browser back-button caching of protected pages.
   - `/logout` endpoint clears session and redirects to `/login`.

5. **Dynamic Current User Information**:
   - Context processor injects `current_user` into all templates.
   - Displays real authenticated user's name, email, role, and initials in top navigation and sidebar.
   - Hardcoded user information completely removed.

6. **All 9 Working Sidebar Module Pages**:
   - Fixed the navigation issue from Milestone 1 where sidebar items did not open.
   - Reusable `dashboard_base.html` template highlights active menu item.
   - Dedicated routes and pages for:
     - `/dashboard`
     - `/content-analytics`
     - `/audience-analytics`
     - `/growth-trends`
     - `/revenue`
     - `/platforms`
     - `/reports`
     - `/notifications`
     - `/settings`
   - Every page supports Dark/Light mode and has clear placeholder architecture sections.

---

## Application Routes

| Route | Access | Description |
|---|---|---|
| `/` | Public | Marketing Landing Page |
| `/login` | Public | User Login Page |
| `/register` | Public | User Registration Page |
| `/logout` | Authenticated | Clears session & logs user out |
| `/dashboard` | **Protected** | Main Analytics Command Center |
| `/content-analytics` | **Protected** | Content performance, reach & engagement |
| `/audience-analytics` | **Protected** | Demographics, active hours & follower churn |
| `/growth-trends` | **Protected** | Growth monitoring & trend detection |
| `/revenue` | **Protected** | Multi-stream revenue & sponsorship analytics |
| `/platforms` | **Protected** | Connected platform management |
| `/reports` | **Protected** | Reports & document exports |
| `/notifications` | **Protected** | Alerts & activity feed |
| `/settings` | **Protected** | Account & application settings |

---

## Installation & Running Instructions

### 1. Configure Environment Variables
Copy `.env.example` to `.env` and set your MySQL credentials:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here

# MySQL Connection (Set your local MySQL root password):
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/creatoriq_db

# Or granular settings:
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DB=creatoriq_db
```

### 2. Create the MySQL Database (One-time setup in MySQL)
Open your MySQL terminal or MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS creatoriq_db;
```

### 3. Run Automated Tests
```bash
python -m unittest tests/test_milestone2.py
```
*All 12 test cases will run and pass.*

### 4. Start the Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Future Project Roadmap

- **Milestone 3: Social Media API Integrations**
  - OAuth 2.0 flow for YouTube Data API v3.
  - Instagram Graph API connection.
  - LinkedIn Marketing & Community Management API integration.
  - Token storage and refresh mechanics.

- **Milestone 4: Real Analytics & Revenue Logic**
  - Automated sync jobs for fetching real metrics.
  - Channel growth calculation algorithms and engagement indexing.
  - Cross-platform revenue calculations and benchmarks.
  - Exportable PDF and Excel performance reports.

- **Milestone 5: Production Deployment & Notifications**
  - Cloud deployment configuration.
  - In-app notification center and alert triggers.
  - Production hardening.
