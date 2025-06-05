#!/usr/bin/env python
"""
Test runner for django-migrate-fresh
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)

    # Run specific test modules if provided as arguments
    if len(sys.argv) > 1:
        test_labels = sys.argv[1:]
    else:
        test_labels = ["tests"]

    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()
