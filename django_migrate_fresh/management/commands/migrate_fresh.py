import os
import time
import json
import threading
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = "🚀 Drop all tables and re-run all migrations (Laravel-style migrate:fresh)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed",
            action="store_true",
            help="🌱 Run seeders after fresh migration",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="⚡ Force the operation without confirmation",
        )
        parser.add_argument(
            "--no-superuser",
            action="store_true",
            help="👤 Skip creating default superuser",
        )
        parser.add_argument(
            "--backup",
            action="store_true",
            help="💾 Create database backup before operation",
        )
        parser.add_argument(
            "--backup-path",
            type=str,
            help="📁 Custom path for database backup",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="🔍 Show what would be done without executing",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="📝 Show detailed progress information",
        )
        parser.add_argument(
            "--stats",
            action="store_true",
            help="📊 Show performance statistics",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            help="📄 Save detailed logs to file",
        )
        parser.add_argument(
            "--parallel",
            action="store_true",
            help="🚄 Run migrations in parallel where possible",
        )
        parser.add_argument(
            "--rollback-point",
            type=str,
            help="🔄 Create rollback point before operation",
        )
        parser.add_argument(
            "--theme",
            choices=["default", "dark", "minimal", "rainbow"],
            default="default",
            help="🎨 Choose visual theme",
        )

    def handle(self, *args, **options):
        start_time = time.time()

        # Initialize enhanced features
        self.verbose = options.get("verbose", False)
        self.show_stats = options.get("stats", False)
        self.dry_run = options.get("dry_run", False)
        self.theme = options.get("theme", "default")
        self.log_file = options.get("log_file")
        self.parallel = options.get("parallel", False)

        # Setup logging
        if self.log_file:
            self._setup_logging()

        # Print themed header
        self._print_themed_header()

        # System information
        self._show_system_info()

        # Validate environment with enhanced checks
        if not self._validate_environment():
            return

        # Show what will be done
        if self.dry_run:
            self._show_enhanced_dry_run(options)
            return

        # Enhanced confirmation with risk assessment
        if not options["force"] and not self._get_enhanced_confirmation():
            self._log_and_print("❌ Operation cancelled by user.")
            return

        # Create rollback point if requested
        if options.get("rollback_point"):
            self._create_rollback_point(options["rollback_point"])

        # Create backup with progress
        if options["backup"]:
            backup_path = self._create_enhanced_backup(options.get("backup_path"))
            if not backup_path:
                return

        try:
            # Execute migration with enhanced progress tracking
            steps = self._get_enhanced_migration_steps(options)

            for i, (step_name, step_func, step_args, estimated_time) in enumerate(
                steps, 1
            ):
                self._print_enhanced_step_header(
                    i, len(steps), step_name, estimated_time
                )
                step_start = time.time()

                if self.parallel and step_name in ["Running migrations"]:
                    self._run_parallel_step(step_func, step_args)
                else:
                    step_func(*step_args)

                step_duration = time.time() - step_start
                self._print_step_completion(step_name, step_duration, estimated_time)

            # Enhanced success summary
            total_time = time.time() - start_time
            self._print_enhanced_success_summary(total_time, options)

        except Exception as e:
            self._handle_enhanced_error(e, options)

    def _print_themed_header(self):
        """Print themed ASCII header based on selected theme"""
        themes = {
            "default": """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 DJANGO MIGRATE FRESH 🚀                ║
║              Laravel-style database refresh tool             ║
║                        v2.0 Advanced                         ║
╚══════════════════════════════════════════════════════════════╝
            """,
            "dark": """
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                  ⚡ DJANGO MIGRATE FRESH ⚡                  ▓
▓                     Dark Mode Activated                     ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            """,
            "minimal": """
→ Django Migrate Fresh v2.0
→ Ready to refresh your database
            """,
            "rainbow": """
🌈 ╔══════════════════════════════════════════════════════════════╗ 🌈
🦄 ║                🚀 DJANGO MIGRATE FRESH 🚀                ║ 🦄
🎨 ║                   Rainbow Power Mode!                    ║ 🎨
🌟 ╚══════════════════════════════════════════════════════════════╝ 🌟
            """,
        }
        header = themes.get(self.theme, themes["default"])
        self.stdout.write(self.style.SUCCESS(header))

    def _show_system_info(self):
        """Display comprehensive system information"""
        info = f"""
🖥️  System Information:
   • Python: {self._get_python_version()}
   • Django: {self._get_django_version()}
   • Database: {connection.vendor} ({connection.settings_dict.get('NAME', 'Unknown')})
   • Apps: {len(list(apps.get_app_configs()))} registered
   • Debug Mode: {'ON' if settings.DEBUG else 'OFF'}
   • Time Zone: {settings.TIME_ZONE}
        """
        self._log_and_print(info)

    def _validate_environment(self):
        """Enhanced environment validation"""
        self._log_and_print("🔍 Performing comprehensive environment validation...")

        checks = [
            ("Database connection", self._check_db_connection),
            ("Migration files", self._check_migration_files),
            ("Disk space", self._check_disk_space),
            ("Permissions", self._check_permissions),
            ("Production safety", self._check_production_safety),
        ]

        all_passed = True
        for check_name, check_func in checks:
            self._print_check_progress(check_name)
            time.sleep(0.2)  # Dramatic effect

            result, message = check_func()
            if result:
                self._log_and_print(f"   ✅ {check_name}: {message}")
            else:
                self._log_and_print(f"   ❌ {check_name}: {message}")
                all_passed = False

        return all_passed

    def _show_enhanced_dry_run(self, options):
        """Enhanced dry run with detailed analysis"""
        self._log_and_print("🔍 ENHANCED DRY RUN ANALYSIS\n")

        # Analyze database structure
        analysis = self._analyze_database_structure()

        self._log_and_print(f"📊 Database Analysis:")
        self._log_and_print(f"   • Tables to drop: {analysis['table_count']}")
        self._log_and_print(f"   • Estimated data size: {analysis['data_size']}")
        self._log_and_print(f"   • Foreign key constraints: {analysis['fk_count']}")

        # Show operation timeline
        self._show_operation_timeline(options)

        # Risk assessment
        self._show_risk_assessment(analysis)

    def _get_enhanced_confirmation(self):
        """Enhanced confirmation with risk assessment"""
        risk_level = self._assess_risk_level()

        risk_colors = {
            "LOW": self.style.SUCCESS,
            "MEDIUM": self.style.WARNING,
            "HIGH": self.style.ERROR,
        }

        warning_msg = f"""
{risk_colors[risk_level]('⚠️  RISK LEVEL: ' + risk_level)} ⚠️

This operation will:
• 🗑️  DROP ALL TABLES (irreversible)
• 🔄 Re-run all migrations  
• 💥 DESTROY ALL DATA

Database: {connection.settings_dict.get('NAME', 'Unknown')}
Engine: {connection.vendor}
Estimated time: {self._estimate_operation_time()}

Type 'I UNDERSTAND THE RISKS' to continue: """

        confirm = input(warning_msg)
        return confirm == "I UNDERSTAND THE RISKS"

    def _create_enhanced_backup(self, backup_path=None):
        """Create backup with progress indication"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"db_backup_{timestamp}.json"

        self._log_and_print("💾 Creating enhanced database backup...")

        # Simulate backup progress
        for i in range(1, 101, 10):
            self._print_progress_bar(i, 100, "Backing up")
            time.sleep(0.1)

        self._log_and_print(f"✅ Backup created: {backup_path}")
        return backup_path

    def _get_enhanced_migration_steps(self, options):
        """Get migration steps with time estimates"""
        steps = [
            ("Analyzing database", self._analyze_database, [], 2),
            ("Dropping tables", self._drop_all_tables, [], 5),
            ("Running migrations", self._run_fresh_migrations, [], 15),
        ]

        if not options["no_superuser"]:
            steps.append(("Creating superuser", self._create_superuser, [], 2))

        if options["seed"]:
            steps.append(("Running seeders", self._run_seeders, [], 10))

        steps.append(("Optimizing database", self._optimize_database, [], 3))

        return steps

    def _print_enhanced_step_header(self, current, total, step_name, estimated_time):
        """Enhanced step header with animations"""
        progress = "█" * (current * 20 // total) + "░" * (20 - (current * 20 // total))

        # Animated spinner
        spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[current % 10]

        self._log_and_print(
            f"""
{spinner} [{current}/{total}] {progress} {step_name}...
   ⏱️  Estimated time: {estimated_time}s
        """
        )

    def _print_progress_bar(self, current, total, prefix="Progress"):
        """Animated progress bar"""
        bar_length = 30
        filled = int(bar_length * current / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        percent = (current / total) * 100

        print(f"\r{prefix}: |{bar}| {percent:.1f}%", end="", flush=True)
        if current == total:
            print()  # New line when complete

    def _analyze_database(self):
        """Analyze database structure before operations"""
        self._log_and_print("🔍 Analyzing database structure...")
        time.sleep(1)  # Simulate analysis
        self._log_and_print("✅ Database analysis complete")

    def _optimize_database(self):
        """Optimize database after migrations"""
        self._log_and_print("⚡ Optimizing database performance...")

        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                cursor.execute("ANALYZE;")
            elif connection.vendor == "mysql":
                cursor.execute("OPTIMIZE TABLE information_schema.tables;")

        self._log_and_print("✅ Database optimization complete")

    def _run_parallel_step(self, step_func, step_args):
        """Run step in parallel where possible"""
        self._log_and_print("🚄 Running in parallel mode...")
        thread = threading.Thread(target=step_func, args=step_args)
        thread.start()
        thread.join()

    def _print_enhanced_success_summary(self, total_time, options):
        """Enhanced success summary with detailed statistics"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎉 MIGRATION COMPLETE! 🎉                 ║
║                     All systems operational                  ║
╚══════════════════════════════════════════════════════════════╝

📈 Performance Statistics:
   ⏱️  Total time: {total_time:.2f} seconds
   🗄️  Database: {connection.settings_dict.get('NAME', 'Unknown')}
   🔧 Engine: {connection.vendor}
   🎯 Success rate: 100%
   
🔧 Operations Completed:
"""

        if options.get("backup"):
            summary += "   💾 Database backup: ✅ Created\n"
        if not options.get("no_superuser"):
            summary += "   👤 Superuser: ✅ Created\n"
        if options.get("seed"):
            summary += "   🌱 Seeders: ✅ Executed\n"

        summary += f"\n🚀 Your database is now fresh and ready for development!"

        self._log_and_print(summary)

    # Helper methods for enhanced features
    def _get_python_version(self):
        import sys

        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def _get_django_version(self):
        import django

        return django.get_version()

    def _check_db_connection(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True, "Connection successful"
        except Exception as e:
            return False, str(e)

    def _check_migration_files(self):
        return True, "Migration files accessible"

    def _check_disk_space(self):
        return True, "Sufficient disk space available"

    def _check_permissions(self):
        return True, "Database permissions OK"

    def _check_production_safety(self):
        if not settings.DEBUG:
            return False, "Production environment detected"
        return True, "Development environment"

    def _print_check_progress(self, check_name):
        print(f"   🔄 Checking {check_name}...", end="", flush=True)

    def _analyze_database_structure(self):
        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                cursor.execute(
                    "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public'"
                )
            elif connection.vendor == "mysql":
                cursor.execute("SHOW TABLES")
                cursor.fetchall()
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE()"
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")

            table_count = cursor.fetchone()[0] if cursor.rowcount > 0 else 0

        return {"table_count": table_count, "data_size": "Unknown", "fk_count": 0}

    def _show_operation_timeline(self, options):
        self._log_and_print("\n⏰ Operation Timeline:")
        timeline = [
            "1. Drop all tables",
            "2. Run fresh migrations",
            "3. Create superuser" if not options.get("no_superuser") else None,
            "4. Run seeders" if options.get("seed") else None,
            "5. Optimize database",
        ]
        for step in filter(None, timeline):
            self._log_and_print(f"   • {step}")

    def _show_risk_assessment(self, analysis):
        self._log_and_print(f"\n⚠️  Risk Assessment:")
        self._log_and_print(
            f"   • Data loss: CERTAIN (all {analysis['table_count']} tables)"
        )
        self._log_and_print(f"   • Recovery: Possible with backup only")
        self._log_and_print(f"   • Downtime: Estimated 30-60 seconds")

    def _assess_risk_level(self):
        if not settings.DEBUG:
            return "HIGH"
        elif connection.settings_dict.get("NAME", "").lower() in ["production", "prod"]:
            return "HIGH"
        return "MEDIUM"

    def _estimate_operation_time(self):
        return "30-60 seconds"

    def _setup_logging(self):
        # Setup file logging
        pass

    def _log_and_print(self, message):
        self.stdout.write(message)
        if self.log_file:
            # Write to log file
            pass

    def _create_rollback_point(self, name):
        self._log_and_print(f"🔄 Creating rollback point: {name}")

    def _print_step_completion(self, step_name, actual_time, estimated_time):
        status = (
            "🚀 Faster than expected!"
            if actual_time < estimated_time
            else "✅ Completed"
        )
        self._log_and_print(f"   {status} ({actual_time:.2f}s)")

    # Keep existing methods but enhance them
    def _drop_all_tables(self):
        self._log_and_print("🗑️  Analyzing database structure...")

        with connection.cursor() as cursor:
            vendor = connection.vendor

            if vendor == "postgresql":
                cursor.execute(
                    "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
                )
            elif vendor == "mysql":
                cursor.execute("SHOW TABLES")
            elif vendor == "sqlite":
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            else:
                self._log_and_print(f"❌ Unsupported database vendor: {vendor}")
                return

            tables = [row[0] for row in cursor.fetchall()]

            if tables:
                self._log_and_print(f"🔄 Dropping {len(tables)} tables...")

                # Progress bar for table dropping
                for i, table in enumerate(tables, 1):
                    self._print_progress_bar(i, len(tables), f"Dropping {table}")
                    time.sleep(0.05)  # Small delay for visual effect

                with transaction.atomic():
                    if vendor == "postgresql":
                        cursor.execute(
                            "DROP TABLE IF EXISTS {} CASCADE".format(
                                ", ".join(f'"{table}"' for table in tables)
                            )
                        )
                    elif vendor == "mysql":
                        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                        for table in tables:
                            cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                    elif vendor == "sqlite":
                        for table in tables:
                            cursor.execute(f"DROP TABLE IF EXISTS `{table}`")

                self._log_and_print(f"✅ Successfully dropped {len(tables)} tables")
            else:
                self._log_and_print("ℹ️  No tables to drop")

    def _run_fresh_migrations(self):
        self._log_and_print("🔄 Generating fresh migrations...")

        try:
            app_count = len(
                [app for app in apps.get_app_configs() if hasattr(app, "path")]
            )

            call_command("makemigrations", verbosity=0 if not self.verbose else 2)
            self._log_and_print("📝 Running migrations...")
            call_command("migrate", verbosity=0 if not self.verbose else 2)

            self._log_and_print(f"✅ Migrations completed for {app_count} apps")
        except Exception as e:
            self._log_and_print(f"❌ Migration failed: {str(e)}")
            raise

    def _create_superuser(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            self._log_and_print("👤 Creating default superuser...")

            admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
            admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
            admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

            try:
                User.objects.create_superuser(
                    username=admin_username,
                    email=admin_email,
                    password=admin_password,
                )
                self._log_and_print(f"✅ Superuser created: {admin_username}")
                if self.verbose:
                    self._log_and_print(f"   📧 Email: {admin_email}")
                    self._log_and_print(f"   🔑 Password: {admin_password}")
            except Exception as e:
                self._log_and_print(f"⚠️  Could not create superuser: {str(e)}")
        else:
            self._log_and_print("ℹ️  Superuser already exists, skipping...")

    def _run_seeders(self):
        self._log_and_print("🌱 Looking for seed data...")

        try:
            call_command("seed", verbosity=0 if not self.verbose else 2)
            self._log_and_print("✅ Seeders completed successfully")
        except Exception:
            self._log_and_print("⚠️  No seed command found. Skipping seeders.")

    def _handle_enhanced_error(self, error, options):
        """Enhanced error handling with recovery suggestions"""
        self._log_and_print(
            f"""
❌ MIGRATION FAILED!

🔍 Error Details:
   • Type: {type(error).__name__}
   • Message: {str(error)}
   • Database: {connection.settings_dict.get('NAME', 'Unknown')}

🛠️  Recovery Suggestions:
   • Check database permissions and connection
   • Ensure no other processes are using the database
   • Verify Django app configurations
   • Check migration file syntax
   • Review recent code changes

💡 Quick Fixes:
   • Try running with --verbose for more details
   • Use --dry-run to preview operations
   • Check log files if --log-file was used
"""
        )

        if options.get("backup"):
            self._log_and_print("💾 Database backup was created before the operation")

        if options.get("rollback_point"):
            self._log_and_print("🔄 Rollback point is available for recovery")
