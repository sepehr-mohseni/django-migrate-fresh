from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-migrate-fresh",
    version="3.0.0",
    author="Sepehr Mohseni",
    author_email="isepehrmohseni@gmail.com",
    description="Enterprise-grade Django package with AI-powered migrate:fresh functionality, comprehensive monitoring, and production-ready security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sepehr-mohseni/django-migrate-fresh",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "psutil>=5.8.0",
    ],
    extras_require={
        "testing": [
            "coverage>=6.0",
            "coveralls>=3.0",
            "pytest>=6.0",
            "pytest-django>=4.0",
            "pytest-cov>=3.0",
        ],
        "notifications": ["requests>=2.25.0", "slack-sdk>=3.0.0"],
        "profiling": ["psutil>=5.8.0", "memory-profiler>=0.60.0"],
        "all": [
            "coverage>=6.0",
            "coveralls>=3.0",
            "pytest>=6.0",
            "pytest-django>=4.0",
            "pytest-cov>=3.0",
            "requests>=2.25.0",
            "slack-sdk>=3.0.0",
            "psutil>=5.8.0",
            "memory-profiler>=0.60.0",
        ],
    },
    keywords="django, migration, laravel, artisan, migrate, fresh, ai, enterprise, monitoring, performance",
)
