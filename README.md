# Django Migrate Fresh 🚀

An advanced Django package that provides Laravel-style `migrate:fresh` functionality with powerful features, beautiful interface, and comprehensive safety measures.

## ✨ Features

### 🎨 Beautiful Interface

- **4 Visual Themes**: Default, Dark, Minimal, Rainbow
- **Animated Progress Bars**: Real-time operation tracking
- **Colored Output**: Easy-to-read status indicators
- **ASCII Art Headers**: Professional command-line experience

### 🛡️ Advanced Safety

- **Risk Assessment**: Automatic environment risk evaluation
- **Enhanced Confirmations**: Multi-level safety prompts
- **Production Detection**: Prevents accidental production runs
- **Rollback Points**: Create recovery checkpoints
- **Comprehensive Backups**: Database backup with progress tracking

### 📊 Performance & Monitoring

- **Real-time Statistics**: Performance timing for each operation
- **Parallel Processing**: Speed up migrations where possible
- **System Information**: Detailed environment analysis
- **Progress Tracking**: Visual progress indicators
- **Detailed Logging**: File-based operation logs

### 🔧 Database Support

- **Multi-Database**: PostgreSQL, MySQL, SQLite
- **Smart Detection**: Automatic database vendor detection
- **Optimization**: Post-migration database optimization
- **Constraint Handling**: Proper foreign key management

## 🚀 Installation

```bash
pip install django-migrate-fresh
```

## 📖 Usage

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your apps
    'django_migrate_fresh',
]
```

### Basic Usage

```bash
# Standard fresh migration
python manage.py migrate_fresh

# Force without confirmation (use with caution!)
python manage.py migrate_fresh --force
```

### 🎨 Visual Themes

```bash
# Dark theme for terminal users
python manage.py migrate_fresh --theme dark

# Minimal output for CI/CD
python manage.py migrate_fresh --theme minimal

# Fun rainbow theme
python manage.py migrate_fresh --theme rainbow
```

### 🛡️ Safety Features

```bash
# Preview changes without executing
python manage.py migrate_fresh --dry-run

# Create backup before operation
python manage.py migrate_fresh --backup

# Custom backup location
python manage.py migrate_fresh --backup --backup-path="/path/to/backup.sql"

# Create rollback point
python manage.py migrate_fresh --rollback-point "before-major-changes"
```

### 📊 Monitoring & Logging

```bash
# Verbose output with detailed information
python manage.py migrate_fresh --verbose

# Show performance statistics
python manage.py migrate_fresh --stats

# Save detailed logs to file
python manage.py migrate_fresh --log-file="migration.log"

# Enable parallel processing
python manage.py migrate_fresh --parallel
```

### 🌱 Seeding & User Management

```bash
# Run with seeders
python manage.py migrate_fresh --seed

# Skip superuser creation
python manage.py migrate_fresh --no-superuser

# Complete setup with all features
python manage.py migrate_fresh --backup --seed --stats --verbose
```

## ⚙️ Configuration

### Environment Variables

Control default superuser creation:

```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### All Available Options

| Option                  | Description                                    |
| ----------------------- | ---------------------------------------------- |
| `--force`               | ⚡ Skip confirmation prompts                   |
| `--seed`                | 🌱 Run seeders after migration                 |
| `--no-superuser`        | 👤 Skip creating default superuser             |
| `--backup`              | 💾 Create database backup                      |
| `--backup-path PATH`    | 📁 Custom backup location                      |
| `--dry-run`             | 🔍 Preview without executing                   |
| `--verbose`             | 📝 Detailed progress information               |
| `--stats`               | 📊 Show performance statistics                 |
| `--log-file PATH`       | 📄 Save logs to file                           |
| `--parallel`            | 🚄 Enable parallel processing                  |
| `--rollback-point NAME` | 🔄 Create rollback checkpoint                  |
| `--theme THEME`         | 🎨 Visual theme (default/dark/minimal/rainbow) |

## 🔥 Advanced Examples

### Development Workflow

```bash
# Complete development reset with all safety features
python manage.py migrate_fresh \
    --backup \
    --seed \
    --verbose \
    --stats \
    --theme dark \
    --log-file "dev-reset.log"
```

### CI/CD Pipeline

```bash
# Minimal output for automated environments
python manage.py migrate_fresh \
    --force \
    --no-superuser \
    --theme minimal \
    --parallel
```

### Production-Like Testing

```bash
# Maximum safety for production-like environments
python manage.py migrate_fresh \
    --backup \
    --rollback-point "pre-deployment-test" \
    --verbose \
    --stats \
    --log-file "production-test.log"
```

## ⚠️ Safety Warnings

**This command will DROP ALL TABLES and destroy all data!**

### Built-in Protection:

- ✅ **Environment Detection**: Automatically detects production environments
- ✅ **Risk Assessment**: Evaluates operation risk level
- ✅ **Enhanced Confirmations**: Multi-step confirmation process
- ✅ **Backup Creation**: Optional database backups
- ✅ **Dry Run Mode**: Preview changes before execution
- ✅ **Rollback Points**: Create recovery checkpoints

### Risk Levels:

- 🟢 **LOW**: Development environment with DEBUG=True
- 🟡 **MEDIUM**: Development environment with production-like settings
- 🔴 **HIGH**: Production environment or production database names

## 🗄️ Supported Databases

| Database       | Support Level | Features                                 |
| -------------- | ------------- | ---------------------------------------- |
| **PostgreSQL** | ✅ Full       | CASCADE drops, ANALYZE optimization      |
| **MySQL**      | ✅ Full       | Foreign key handling, table optimization |
| **SQLite**     | ✅ Full       | File-based operations                    |

## 🚀 What's New in v2.0

- 🎨 **4 Visual Themes** with beautiful ASCII art
- 📊 **Real-time Progress Bars** and performance statistics
- 🛡️ **Enhanced Safety Features** with risk assessment
- 🚄 **Parallel Processing** for faster operations
- 📄 **Comprehensive Logging** to files
- 🔄 **Rollback Points** for recovery
- 🔍 **Advanced Dry Run** with detailed analysis
- ⚡ **Database Optimization** post-migration
- 🌍 **Multi-environment Support** with smart detection

## 📚 Documentation

For detailed documentation, examples, and advanced usage:

🔗 **https://github.com/sepehr-mohseni/django-migrate-fresh**

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines in the repository.

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for the Django community**
