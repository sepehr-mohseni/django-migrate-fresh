from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-migrate-fresh",
    version="2.0.0",
    author="Sepehr Mohseni",
    author_email="isepehrmohseni@gmail.com",
    description="Advanced Django package with Laravel-style migrate:fresh functionality, beautiful themes, and comprehensive safety features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sepehr-mohseni/django-migrate-fresh",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
    ],
    keywords="django, migration, laravel, artisan, migrate, fresh",
)
