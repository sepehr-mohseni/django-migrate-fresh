"""
Test settings for django-migrate-fresh
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key-for-django-migrate-fresh"

DEBUG = True

ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_migrate_fresh",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

USE_TZ = True

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Test-specific settings
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Ensure command attributes are properly initialized for tests
import django_migrate_fresh.management.commands.migrate_fresh

# Monkey patch to ensure attributes exist
original_init = django_migrate_fresh.management.commands.migrate_fresh.Command.__init__


def patched_init(self, *args, **kwargs):
    result = (
        original_init(self, *args, **kwargs)
        if hasattr(
            django_migrate_fresh.management.commands.migrate_fresh.Command, "__init__"
        )
        else None
    )
    # Initialize all required attributes for tests
    self.verbose = False
    self.show_stats = False
    self.dry_run = False
    self.theme = "default"
    self.log_file = None
    self.parallel = False
    self.interactive = False
    self.benchmark = False
    self.profile = False
    self.ai_mode = False
    self.cache_enabled = False
    self.performance_mode = False
    return result


django_migrate_fresh.management.commands.migrate_fresh.Command.__init__ = patched_init
