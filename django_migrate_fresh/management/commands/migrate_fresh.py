import os
import time
from datetime import datetime
from typing import Any, Dict
from argparse import ArgumentParser

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = "🚀 Drop all tables and re-run all migrations (Laravel-style migrate:fresh)"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="⚡ Force the operation without confirmation",
        )
        parser.add_argument(
            "--backup",
            action="store_true",
            help="💾 Create database backup before operation",
        )
        parser.add_argument(
            "--backup-path", type=str, help="📁 Custom path for database backup"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(self.style.SUCCESS("\n🚀 Django Migrate Fresh\n" + "=" * 50))

        # Check if backup is wanted
        backup_needed = options.get("backup", False)
        backup_path = options.get("backup_path", "")

        if not backup_needed and not options.get("force"):
            backup_response = input(
                "\n💾 Do you want to create a backup before proceeding? [y/N]: "
            ).lower()
            if backup_response in ["y", "yes"]:
                backup_needed = True

        if backup_needed and not backup_path:
            default_backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            backup_path = input(f"\n📁 Enter backup path [{default_backup}]: ").strip()
            if not backup_path:
                backup_path = default_backup

        # Create backup if requested
        if backup_needed:
            try:
                self._create_backup(backup_path)
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Backup created: {backup_path}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Backup failed: {str(e)}"))
                return

        # Show confirmation
        if not options.get("force"):
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️  This will DROP ALL TABLES and re-run migrations."
                )
            )
            response = input("\n🤔 Are you sure you want to continue? [y/N]: ").lower()
            if response not in ["y", "yes"]:
                self.stdout.write(self.style.SUCCESS("❌ Operation cancelled."))
                return

        # Execute the migration fresh
        start_time = time.time()
        try:
            self._execute_fresh_migration()
            execution_time = time.time() - start_time

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ Migration completed successfully in {execution_time:.2f} seconds!"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Migration failed: {str(e)}"))
            raise

    def _create_backup(self, backup_path: str) -> None:
        """Create a simple database backup"""
        self.stdout.write("💾 Creating backup...")

        db_settings = connection.settings_dict

        if connection.vendor == "postgresql":
            # PostgreSQL backup
            cmd = [
                "pg_dump",
                f"--host={db_settings['HOST']}",
                f"--port={db_settings['PORT']}",
                f"--username={db_settings['USER']}",
                f"--dbname={db_settings['NAME']}",
                f"--file={backup_path}",
                "--no-password",
            ]
        elif connection.vendor == "mysql":
            # MySQL backup
            cmd = [
                "mysqldump",
                f"--host={db_settings['HOST']}",
                f"--port={db_settings['PORT']}",
                f"--user={db_settings['USER']}",
                f"--password={db_settings['PASSWORD']}",
                db_settings["NAME"],
                f"--result-file={backup_path}",
            ]
        elif connection.vendor == "sqlite":
            # SQLite backup (simple file copy)
            import shutil

            shutil.copy2(db_settings["NAME"], backup_path)
            return
        else:
            raise CommandError(f"Backup not supported for {connection.vendor}")

        # Execute backup command
        import subprocess

        env = os.environ.copy()
        if connection.vendor == "postgresql" and db_settings.get("PASSWORD"):
            env["PGPASSWORD"] = db_settings["PASSWORD"]

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            raise CommandError(f"Backup command failed: {result.stderr}")

    def _execute_fresh_migration(self) -> None:
        """Execute the fresh migration process"""
        self.stdout.write("🔥 Dropping all tables...")

        # Drop all tables
        self._drop_all_tables()

        self.stdout.write("🏗️  Running migrations...")

        # Run migrations
        call_command("migrate", verbosity=0)

        self.stdout.write("✨ Fresh migration completed!")

    def _drop_all_tables(self) -> None:
        """Drop all database tables"""
        with connection.cursor() as cursor:
            # Get list of tables
            if connection.vendor == "postgresql":
                cursor.execute(
                    """
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """
                )
            elif connection.vendor == "mysql":
                cursor.execute("SHOW TABLES")
            elif connection.vendor == "sqlite":
                cursor.execute(
                    """
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name != 'sqlite_sequence'
                """
                )
            else:
                raise CommandError(
                    f"Database vendor '{connection.vendor}' not supported"
                )

            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                self.stdout.write("ℹ️  No tables to drop")
                return

            # Drop tables
            if connection.vendor == "postgresql":
                # Disable foreign key checks and drop all tables
                cursor.execute(f"DROP TABLE IF EXISTS {', '.join(tables)} CASCADE")
            elif connection.vendor == "mysql":
                # Disable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            elif connection.vendor == "sqlite":
                # SQLite: disable foreign key constraints, drop tables, re-enable
                cursor.execute("PRAGMA foreign_keys = OFF")
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                cursor.execute("PRAGMA foreign_keys = ON")

            self.stdout.write(f"🗑️  Dropped {len(tables)} tables")
