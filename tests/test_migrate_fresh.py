from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.management.base import CommandError
from django.db import connection
from django_migrate_fresh.management.commands.migrate_fresh import Command


class MigrateFreshTestCase(TestCase):
    def setUp(self):
        self.command = Command()

    def test_help_message(self):
        """Test command help message"""
        self.assertIn("🚀 Drop all tables", self.command.help)

    def test_add_arguments(self):
        """Test command arguments are added correctly"""
        parser = MagicMock()
        self.command.add_arguments(parser)

        # Should have called add_argument 3 times for --force, --backup, --backup-path
        self.assertEqual(parser.add_argument.call_count, 3)

    @patch.object(Command, "_create_backup")
    @patch.object(Command, "_execute_fresh_migration")
    def test_handle_with_backup_and_force(self, mock_execute, mock_backup):
        """Test execution with backup option and force"""
        self.command.handle(backup=True, backup_path="test.sql", force=True)

        mock_backup.assert_called_once_with("test.sql")
        mock_execute.assert_called_once()

    def test_create_backup_unsupported_vendor(self):
        """Test backup with unsupported database vendor raises error"""
        with patch.object(connection, "vendor", "unsupported"):
            with self.assertRaises(CommandError):
                self.command._create_backup("test.sql")

    @patch("shutil.copy2")
    def test_create_backup_sqlite(self, mock_copy):
        """Test SQLite backup creation"""
        with patch.object(connection, "vendor", "sqlite"):
            with patch.object(
                connection, "settings_dict", {"NAME": "/path/to/db.sqlite3"}
            ):
                self.command._create_backup("test.sql")
                mock_copy.assert_called_once()

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    @patch.object(Command, "_drop_all_tables")
    def test_execute_fresh_migration(self, mock_drop, mock_call_command):
        """Test fresh migration execution"""
        self.command._execute_fresh_migration()

        mock_drop.assert_called_once()
        mock_call_command.assert_called_once_with("migrate", verbosity=0)

    def test_drop_all_tables_unsupported_vendor(self):
        """Test dropping tables with unsupported vendor raises error"""
        with patch.object(connection, "vendor", "unsupported"):
            with self.assertRaises(CommandError):
                self.command._drop_all_tables()
