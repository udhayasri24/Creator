# CreatorIQ — Creator Analytics & Content Performance Dashboard

A centralized analytics platform where creators can monitor YouTube, Instagram, and LinkedIn channels to view content performance, audience analytics, growth trends, revenue analytics, reports, notifications, and platform comparisons from one unified command center.

---

## Current Milestone: Milestone 1 (Foundation & UI Shell)

> **Important Note:**  
> This project follows a milestone-based roadmap. **Milestone 1** implements the project foundation, clean Flask architecture, database configuration with SQLAlchemy for MySQL, and complete modern UI shell with dynamic Dark/Light theme switching and Chart.js visualizations.
> 
> *Social media API integrations (YouTube, Instagram, LinkedIn OAuth), backend authentication, database migrations, real analytics processing, PDF/Excel reports, and cloud deployment are scheduled for subsequent milestones.*

---

## Technology Stack (Milestone 1)

### Frontend
- **HTML5**: Semantic document structuring
- **CSS3**: Vanilla CSS design system with CSS custom properties (variables) for instant Dark/Light mode switching
- **JavaScript**: Vanilla ES6+ for theme persistence (`localStorage`), mobile sidebar drawer, and chart updates
- **Chart.js (4.4)**: Interactive canvas visualizations for follower growth, views, engagement, and platform shares

### Backend
- **Python (3.13+)**: Application logic
- **Flask (3.1+)**: Clean, lightweight WSGI web framework using the Application Factory & Blueprints pattern

### Database & ORM
- **MySQL**: Relational database engine (configured for Milestone 2+ persistence)
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
|  - Blueprints:                                                  |
|      * main_bp      -> Landing Page (/)                         |
|      * auth_bp      -> Login & Register UI (/login, /register)  |
|      * dashboard_bp -> Analytics Shell (/dashboard)             |
+-----------------------------------------------------------------+
                                |
                      Database Configuration
                                ↓
+-----------------------------------------------------------------+
|                   SQLAlchemy ORM Layer                          |
|  - config.py (Config, DevelopmentConfig, ProductionConfig)      |
|  - database/__init__.py (db instance)                           |
|  - models/__init__.py (User, PlatformAccount schemas ready)     |
+-----------------------------------------------------------------+
                                |
                         PyMySQL Connector
                                ↓
+-----------------------------------------------------------------+
|                         MySQL Database                          |
|  (Connection configured via DATABASE_URL or .env credentials)   |
+-----------------------------------------------------------------+

Future Architecture (Milestones 2 & 3+):
Browser <-> Flask Backend <-> Social Media APIs (YouTube/Instagram/LinkedIn) <-> MySQL
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
├── models/                 # ORM Database Models (Milestone 2 preparation)
│   └── __init__.py         # User and PlatformAccount schema definitions
│
├── routes/                 # Modular Blueprint Routes
│   ├── __init__.py         # Blueprint registration logic
│   ├── main_routes.py      # Landing page route (/)
│   ├── auth_routes.py      # Login & Register UI routes (/login, /register)
│   └── dashboard_routes.py # Dashboard UI shell route (/dashboard)
│
├── templates/              # Jinja2 HTML Templates
│   ├── base.html           # Master layout with theme engine & Chart.js CDN
│   ├── index.html          # High-converting SaaS landing page
│   ├── login.html          # Login UI page
│   ├── register.html       # Register UI page (with creator roles)
│   └── dashboard.html      # Analytics dashboard shell with KPI cards & charts
│
└── static/                 # Static Assets
    ├── css/
    │   └── style.css       # Unified design system, CSS variables & responsiveness
    └── js/
        └── app.js          # Dark/Light theme manager, sidebar toggle, Chart.js config
```

---

## Features Implemented in Milestone 1

1. **Modern SaaS Landing Page (`/`)**:
   - Hero section with bold value proposition and preview card.
   - Quick platform cards for YouTube, Instagram, and LinkedIn.
   - Core capabilities feature grid.
   - Direct navigation to Login, Register, and Live Dashboard preview.

2. **Dashboard UI Shell (`/dashboard`)**:
   - **Collapsible Sidebar**: Dashboard, Content Analytics, Audience Analytics, Growth & Trends, Revenue, Platforms, Reports, Notifications, Settings.
   - **Top Navigation Bar**: Brand logo, search input, notification icon, user profile widget, and theme toggle button.
   - **Responsive Drawer**: Hamburger toggle on mobile and tablet devices with backdrop dismiss.

3. **Dashboard KPI Metric Cards**:
   - **Total Views**: `125,430` (+14.2% vs last month)
   - **Total Likes**: `18,240` (+8.5% vs last month)
   - **Followers**: `42,850` (+5.1% vs last month)
   - **Engagement Rate**: `8.7%` (+1.8% benchmark)
   - **Total Revenue**: `₹85,400` (+12.3% vs last month)

4. **Interactive Dashboard Charts (Chart.js 4.4)**:
   - **Follower Growth**: Multi-series line chart tracking monthly audience progression.
   - **Views Trend**: Dual-series bar chart for video views and shorts/reels reach.
   - **Engagement Rate**: Curved area chart showing weekly interaction percentages.
   - **Platform Performance**: Doughnut chart showing audience distribution.
   - **Top Performing Content**: Horizontal bar chart with a companion summary table ranking top posts.

5. **Platform Status Section**:
   - Dedicated cards for YouTube, Instagram, and LinkedIn displaying **"Not Connected"** status badge as required for Milestone 1.

6. **Dynamic Theme Engine (Dark & Light Mode)**:
   - Real-time toggle on every page (Landing, Login, Register, Dashboard).
   - Saved across sessions using browser `localStorage`.
   - Inline script prevents flicker/flash on page load.
   - Chart.js grid and label colors adapt dynamically when switching themes.

7. **Login & Register UI**:
   - Clean, focused SaaS authentication interfaces.
   - Register form includes role selection (`Creator`, `Agency`, `Marketing Team`, `Administrator`).
   - One-click shortcuts to explore the demo dashboard.

8. **MySQL & SQLAlchemy Ready**:
   - Environment variables loaded securely from `.env` via `python-dotenv`.
   - `config.py` builds the PyMySQL connection string dynamically without hardcoded secrets.
   - Initialized `db` instance and model outlines in `models/` ready for Milestone 2 migrations.

---

## Installation & Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Git
- MySQL Server (optional for Milestone 1 UI preview; required for Milestone 2 database storage)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd creatoriq24
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```
Open `.env` and configure your settings if you want to connect your local MySQL database:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/creatoriq_db
```

### Step 5: Run the Flask Application
```bash
python app.py
```
Or with Flask CLI:
```bash
flask run --port=5000
```

### Step 6: Open the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Available Application Routes

| Route | Description |
|---|---|
| `http://127.0.0.1:5000/` | CreatorIQ Landing Page |
| `http://127.0.0.1:5000/login` | Login UI Page |
| `http://127.0.0.1:5000/register` | Register UI Page |
| `http://127.0.0.1:5000/dashboard` | Main Analytics Dashboard Shell |
| `http://127.0.0.1:5000/logout` | Demo session sign-out |

---

## Future Project Roadmap

- **Milestone 2: Authentication & User Management**
  - Real user registration and login with password hashing (`Werkzeug` / `bcrypt`).
  - Session handling and Flask-Login integration.
  - Role-based access control (Creator, Agency, Marketing Team, Admin).
  - MySQL database table creation and migrations.

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
  - Cloud deployment configuration (e.g., AWS / Render / GCP).
  - In-app notification center and alert triggers.
  - Performance monitoring and production hardening.
