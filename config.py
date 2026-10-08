"""
Configuration module for CreatorIQ.
Loads environment variables and sets up application configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
# override=True ensures .env values replace any stale/empty inherited environment variables
loaded = load_dotenv(BASE_DIR / ".env", override=True)
if not loaded:
    print(f" [!] WARNING: .env file not found at {BASE_DIR / '.env'}. Using system environment or defaults.")


class Config:
    """Base configuration class."""

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "creatoriq-dev-secret-key-change-in-production")

    # MySQL Database Configuration
    # Uses DATABASE_URL if defined, otherwise constructs from individual MySQL variables
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "creatoriq_db")

    # SQLAlchemy Database URI (defaults to MySQL with PyMySQL connector)
    # Note: These class attributes are resolved after load_dotenv(override=True) above,
    # so they will always reflect the .env values.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug mode flag
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


from sqlalchemy.pool import StaticPool


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False


# Map environment names to config classes
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
