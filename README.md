# Django Migrate Fresh 🚀

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/django-migrate-fresh?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=Installs)](https://pepy.tech/projects/django-migrate-fresh)

A simple Django package that provides Laravel-style `migrate:fresh` functionality - drop all tables and re-run migrations with optional backup support.

## Installation

```bash
pip install django-migrate-fresh
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'django_migrate_fresh',
]
```

## Usage

### Basic Usage

Drop all tables and re-run migrations:

```bash
python manage.py migrate_fresh
```

### With Backup

Create a backup before running:

```bash
python manage.py migrate_fresh --backup
```

Specify backup path:

```bash
python manage.py migrate_fresh --backup --backup-path my_backup.sql
```

### Force Mode (No Confirmations)

Skip all confirmations:

```bash
python manage.py migrate_fresh --force
```

## Command Options

- `--force`: Skip all confirmation prompts
- `--backup`: Create a backup before dropping tables
- `--backup-path PATH`: Specify custom backup file path

## Interactive Mode

When run without `--force`, the command will ask:

1. **Backup confirmation**: "Do you want to create a backup before proceeding?"
2. **Path input** (if backup selected): Prompts for backup file path
3. **Final confirmation**: "Are you sure you want to continue?"

## Database Support

- **PostgreSQL**: Uses `pg_dump` for backups
- **MySQL**: Uses `mysqldump` for backups  
- **SQLite**: Simple file copy for backups

## Example Session

```bash
$ python manage.py migrate_fresh

🚀 Django Migrate Fresh
==================================================

💾 Do you want to create a backup before proceeding? [y/N]: y

📁 Enter backup path [backup_20231219_143022.sql]: my_backup.sql

⚠️  This will DROP ALL TABLES and re-run migrations.

🤔 Are you sure you want to continue? [y/N]: y

💾 Creating backup...
✅ Backup created: my_backup.sql
🔥 Dropping all tables...
🗑️  Dropped 15 tables
🏗️  Running migrations...
✨ Fresh migration completed!

✅ Migration completed successfully in 2.34 seconds!
```

## Requirements

- Django >= 3.2
- Python >= 3.8

## License

MIT License
