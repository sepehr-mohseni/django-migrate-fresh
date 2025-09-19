from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-migrate-fresh",
    version="3.1.0",
    author="Sepehr Mohseni",
    author_email="isepehrmohseni@gmail.com",
    description="Simple Django package for Laravel-style migrate:fresh functionality with backup support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sepehr-mohseni/django-migrate-fresh",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    extras_require={
        "test": [
            "pytest>=6.0",
            "pytest-django>=4.0",
        ],
    },
    keywords="django, migration, laravel, migrate, fresh, backup",
)
