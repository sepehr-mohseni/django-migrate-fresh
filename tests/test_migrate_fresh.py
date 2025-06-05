import os
import json
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock, call
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.contrib.auth import get_user_model
from django_migrate_fresh.management.commands.migrate_fresh import Command


class MigrateFreshTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        from django.core.management.base import OutputWrapper

        self.command.stdout = OutputWrapper(self.out)

    def test_help_message(self):
        """Test command help message"""
        self.assertIn("🚀 Drop all tables", self.command.help)

    def test_add_arguments(self):
        """Test all command arguments are added"""
        parser = MagicMock()
        self.command.add_arguments(parser)

        # Check that essential arguments are added including new AI features
        expected_args = [
            "--force",
            "--seed",
            "--no-superuser",
            "--dry-run",
            "--backup",
            "--verbose",
            "--theme",
            "--interactive",
            "--stats",
            "--benchmark",
            "--profile",
            "--health-check",
            # New AI and performance features
            "--ai",
            "--learn",
            "--predict",
            "--cache",
            "--performance",
            "--adaptive",
        ]

        calls = [call for call in parser.add_argument.call_args_list]
        added_args = [call[0][0] for call in calls]

        for arg in expected_args:
            self.assertIn(arg, added_args)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_initialize_options(self, mock_psutil):
        """Test option initialization"""
        options = {"verbose": True, "theme": "dark", "dry_run": False, "profile": True}

        self.command._initialize_options(options)

        self.assertTrue(self.command.verbose)
        self.assertEqual(self.command.theme, "dark")
        self.assertFalse(self.command.dry_run)
        self.assertTrue(self.command.profile)

    def test_quick_validate_success(self):
        """Test successful database validation"""
        with patch.object(connection, "cursor") as mock_cursor:
            mock_cursor.return_value.__enter__.return_value.execute.return_value = None
            result = self.command._quick_validate()
            self.assertTrue(result)

    def test_quick_validate_failure(self):
        """Test failed database validation"""
        with patch.object(connection, "cursor") as mock_cursor:
            mock_cursor.side_effect = Exception("Connection failed")
            result = self.command._quick_validate()
            self.assertFalse(result)

    def test_themed_headers(self):
        """Test all themed headers"""
        themes = ["default", "dark", "minimal", "rainbow"]

        for theme in themes:
            self.command.theme = theme
            self.command._print_themed_header()
            output = self.out.getvalue()
            # Check for actual content without ANSI codes
            clean_output = output.replace("\x1b[32;1m", "").replace("\x1b[0m", "")
            if theme == "minimal":
                self.assertIn("Django Migrate Fresh", clean_output)
            else:
                self.assertIn("DJANGO MIGRATE FRESH", clean_output)
            self.out = StringIO()
            from django.core.management.base import OutputWrapper

            self.command.stdout = OutputWrapper(self.out)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_system_info_with_psutil(self, mock_psutil):
        """Test system info display with psutil available"""
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.virtual_memory.return_value.total = 16 * 1024**3
        mock_psutil.virtual_memory.return_value.percent = 50.0

        self.command._show_enhanced_system_info()
        output = self.out.getvalue()

        self.assertIn("8 cores", output)
        self.assertIn("16 GB RAM", output)
        self.assertIn("50.0% used", output)

    def test_system_info_without_psutil(self):
        """Test system info display without psutil"""
        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.psutil", None
        ):
            self.command._show_enhanced_system_info()
            output = self.out.getvalue()
            self.assertIn("System monitoring unavailable", output)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_health_check(self, mock_psutil):
        """Test health check functionality"""
        mock_psutil.virtual_memory.return_value.percent = 50.0
        mock_psutil.disk_usage.return_value.free = 10 * 1024**3
        mock_psutil.disk_usage.return_value.total = 100 * 1024**3

        self.command._perform_health_check()
        output = self.out.getvalue()

        self.assertIn("Running health checks", output)
        self.assertIn("Database", output)
        self.assertIn("Memory", output)

    @patch("builtins.input")
    def test_interactive_mode(self, mock_input):
        """Test interactive mode"""
        mock_input.side_effect = ["y", "n", "yes"]

        options = {}
        result = self.command._interactive_mode(options)

        self.assertTrue(result.get("backup"))
        self.assertNotIn("seed", result)
        self.assertTrue(result.get("verbose"))

    def test_create_smart_backup(self):
        """Test smart backup creation"""
        options = {"backup_path": None}
        self.command.verbose = True

        result = self.command._create_smart_backup(options)

        # The method should always return a string
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("backup_"))

        # Check output if verbose
        output = self.out.getvalue()
        if self.command.verbose:
            self.assertIn("Backup created", output)

    def test_get_table_list_postgresql(self):
        """Test table list retrieval for PostgreSQL"""
        with patch.object(connection, "vendor", "postgresql"), patch.object(
            connection, "cursor"
        ) as mock_cursor:

            mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
                ("table1",),
                ("table2",),
                ("table3",),
            ]

            tables = self.command._get_table_list()
            self.assertEqual(tables, ["table1", "table2", "table3"])

    def test_get_table_list_mysql(self):
        """Test table list retrieval for MySQL"""
        with patch.object(connection, "vendor", "mysql"), patch.object(
            connection, "cursor"
        ) as mock_cursor:

            mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
                ("users",),
                ("products",),
            ]

            tables = self.command._get_table_list()
            self.assertEqual(tables, ["users", "products"])

    def test_get_table_list_sqlite(self):
        """Test table list retrieval for SQLite"""
        with patch.object(connection, "vendor", "sqlite"), patch.object(
            connection, "cursor"
        ) as mock_cursor:

            mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
                ("auth_user",),
                ("django_migrations",),
            ]

            tables = self.command._get_table_list()
            self.assertEqual(tables, ["auth_user", "django_migrations"])

    def test_export_schema(self):
        """Test schema export functionality"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            export_path = f.name

        try:
            with patch.object(self.command, "_get_table_list") as mock_get_tables:
                mock_get_tables.return_value = ["table1", "table2"]

                self.command._export_schema(export_path)

                with open(export_path, "r") as f:
                    schema_data = json.load(f)

                self.assertIn("timestamp", schema_data)
                self.assertIn("database", schema_data)
                self.assertEqual(schema_data["tables"], ["table1", "table2"])
        finally:
            os.unlink(export_path)

    def test_compare_schema_file_not_found(self):
        """Test schema comparison with missing file"""
        self.command._compare_schema("/nonexistent/file.json")
        output = self.out.getvalue()
        self.assertIn("Previous schema file not found", output)

    def test_compare_schema_success(self):
        """Test successful schema comparison"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump({"tables": ["old_table1", "old_table2"]}, f)
            compare_path = f.name

        try:
            with patch.object(self.command, "_get_table_list") as mock_get_tables:
                mock_get_tables.return_value = ["table1", "table2", "table3"]

                self.command._compare_schema(compare_path)
                output = self.out.getvalue()

                self.assertIn("Schema comparison", output)
                self.assertIn("Table changes: 1", output)
        finally:
            os.unlink(compare_path)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    def test_drop_tables_postgresql(self, mock_call_command):
        """Test table dropping for PostgreSQL"""
        with patch.object(connection, "vendor", "postgresql"), patch.object(
            connection, "cursor"
        ) as mock_cursor, patch.object(
            self.command, "_get_table_list"
        ) as mock_get_tables:

            mock_get_tables.return_value = ["table1", "table2"]
            self.command.verbose = True
            # Initialize performance_mode attribute
            self.command.performance_mode = False

            self.command._drop_all_tables()

            mock_cursor.return_value.__enter__.return_value.execute.assert_called()

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    def test_run_fresh_migrations(self, mock_call_command):
        """Test migration execution"""
        self.command.verbose = False
        self.command._run_fresh_migrations()

        expected_calls = [
            call("makemigrations", verbosity=0),
            call("migrate", verbosity=0),
        ]

        mock_call_command.assert_has_calls(expected_calls)

    @patch("django.contrib.auth.get_user_model")
    def test_create_superuser_success(self, mock_get_user_model):
        """Test successful superuser creation"""
        mock_user_model = MagicMock()
        mock_user_model.objects.filter.return_value.exists.return_value = False
        mock_user_model.objects.create_superuser = MagicMock()
        mock_get_user_model.return_value = mock_user_model

        with patch.dict(
            os.environ,
            {
                "DJANGO_SUPERUSER_USERNAME": "testadmin",
                "DJANGO_SUPERUSER_EMAIL": "test@example.com",
                "DJANGO_SUPERUSER_PASSWORD": "testpass123",
            },
        ):
            self.command._create_superuser()

        mock_user_model.objects.create_superuser.assert_called_once_with(
            username="testadmin", email="test@example.com", password="testpass123"
        )

    @patch("django.contrib.auth.get_user_model")
    def test_create_superuser_already_exists(self, mock_get_user_model):
        """Test superuser creation when one already exists"""
        mock_user_model = MagicMock()
        mock_user_model.objects.filter.return_value.exists.return_value = True
        mock_get_user_model.return_value = mock_user_model

        self.command._create_superuser()

        mock_user_model.objects.create_superuser.assert_not_called()

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    def test_run_seeders_success(self, mock_call_command):
        """Test successful seeder execution"""
        self.command.verbose = True
        self.command._run_seeders()

        mock_call_command.assert_called_once_with("seed", verbosity=0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    def test_run_seeders_not_found(self, mock_call_command):
        """Test seeder execution when seed command doesn't exist"""
        mock_call_command.side_effect = Exception("No such command")
        self.command.verbose = True

        self.command._run_seeders()
        output = self.out.getvalue()
        self.assertIn("No seeders found", output)

    def test_benchmark_connection(self):
        """Test connection benchmarking"""
        with patch.object(connection, "cursor") as mock_cursor:
            result = self.command._benchmark_connection()
            self.assertTrue(result.endswith("ms"))
            self.assertTrue(float(result[:-2]) >= 0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_profiling(self, mock_psutil):
        """Test performance profiling"""
        mock_process = MagicMock()
        mock_process.memory_info.return_value.rss = 1024 * 1024 * 100  # 100MB
        mock_psutil.Process.return_value = mock_process

        self.command._start_profiling()
        self.assertTrue(hasattr(self.command, "profile_start_time"))

        self.command._stop_profiling()
        output = self.out.getvalue()
        self.assertIn("Profile:", output)

    @patch("builtins.input")
    def test_enhanced_confirmation_yes(self, mock_input):
        """Test user confirmation - yes"""
        mock_input.return_value = "yes"
        result = self.command._get_enhanced_confirmation()
        self.assertTrue(result)

    @patch("builtins.input")
    def test_enhanced_confirmation_no(self, mock_input):
        """Test user confirmation - no"""
        mock_input.return_value = "no"
        result = self.command._get_enhanced_confirmation()
        self.assertFalse(result)

    def test_get_migration_steps_default(self):
        """Test default migration steps"""
        options = {}
        steps = self.command._get_enhanced_migration_steps(options)

        self.assertEqual(len(steps), 3)  # drop, migrate, create_superuser
        step_names = [step[0] for step in steps]
        self.assertIn("Dropping tables", step_names)
        self.assertIn("Running migrations", step_names)
        self.assertIn("Creating superuser", step_names)

    def test_get_migration_steps_with_options(self):
        """Test migration steps with options"""
        options = {"no_superuser": True, "seed": True}
        steps = self.command._get_enhanced_migration_steps(options)

        step_names = [step[0] for step in steps]
        self.assertNotIn("Creating superuser", step_names)
        self.assertIn("Running seeders", step_names)

    @patch("builtins.input")
    def test_dry_run_mode(self, mock_input):
        """Test dry run functionality"""
        self.command.dry_run = True
        self.command._show_enhanced_dry_run({})
        output = self.out.getvalue()
        self.assertIn("DRY RUN", output)

    def test_notification_methods(self):
        """Test notification placeholder methods"""
        # These should not raise exceptions
        self.command._send_slack_notification("test")
        self.command._send_email_notification("test")
        self.command._send_discord_notification("test")
        self.command._send_teams_notification("test")

    def test_send_notification(self):
        """Test notification sending"""
        self.command._send_notification("slack", 1.5)
        output = self.out.getvalue()
        self.assertIn("Would send slack notification", output)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    @patch("builtins.input")
    def test_full_workflow_force(self, mock_input, mock_call_command):
        """Test complete workflow with force option"""
        options = {
            "force": True,
            "verbose": False,
            "dry_run": False,
            "backup": False,
            "smart_backup": False,
            "interactive": False,
            "health_check": False,
            "profile": False,
            "benchmark": False,
        }

        with patch.object(
            self.command, "_quick_validate", return_value=True
        ), patch.object(self.command, "_get_table_list", return_value=["test_table"]):

            self.command.handle(**options)

            # Verify migrations were called
            mock_call_command.assert_called()

    def test_error_handling(self):
        """Test error handling"""
        error = Exception("Test error")
        self.command._handle_enhanced_error(error, {})
        output = self.out.getvalue()
        self.assertIn("Error: Test error", output)


class FeatureComplianceTestCase(TestCase):
    """Test that all features mentioned in README are implemented"""

    def setUp(self):
        self.command = Command()

    def test_all_readme_features_implemented(self):
        """Verify all README features are actually implemented"""
        # Core features from README including new AI features
        core_features = [
            "_interactive_mode",  # Interactive Experience
            "_print_themed_header",  # 4 Visual Themes
            "_create_smart_backup",  # Smart Backup
            "_auto_optimize_database",  # Auto-Optimization
            "_perform_health_check",  # Health Monitoring
            "_run_benchmarks",  # Performance Benchmarking
            "_start_profiling",  # Resource Profiling
            "_export_schema",  # Schema Export
            "_compare_schema",  # Schema Comparison
            "_send_notification",  # Notifications
            # New AI features
            "_ai_analyze_migration",  # AI Analysis
            "_ai_estimate_migration_time",  # AI Time Estimation
            "_ai_assess_risk",  # AI Risk Assessment
            "_adaptive_optimization",  # Adaptive Optimization
            "_execute_parallel_workflow",  # Parallel Processing
            "_ai_optimize_step_order",  # AI Step Optimization
            "_ai_learn_from_migration",  # AI Learning
        ]

        for feature in core_features:
            self.assertTrue(
                hasattr(self.command, feature), f"Feature {feature} not implemented"
            )

    def test_all_command_arguments_from_readme(self):
        """Test that all command arguments from README are available"""
        from argparse import ArgumentParser

        parser = ArgumentParser()
        self.command.add_arguments(parser)

        # Arguments mentioned in README including new features
        readme_args = [
            "force",
            "seed",
            "no_superuser",
            "dry_run",
            "backup",
            "smart_backup",
            "encrypt",
            "compress",
            "verbose",
            "theme",
            "interactive",
            "stats",
            "parallel",
            "benchmark",
            "profile",
            "auto_optimize",
            "health_check",
            "export_schema",
            "compare_schema",
            "notify",
            # New AI and performance features
            "ai",
            "learn",
            "predict",
            "cache",
            "performance",
            "adaptive",
        ]

        # Get all added arguments
        added_args = []
        for action in parser._actions:
            if hasattr(action, "option_strings"):
                for opt in action.option_strings:
                    if opt.startswith("--"):
                        added_args.append(opt[2:].replace("-", "_"))

        for arg in readme_args:
            self.assertIn(
                arg,
                added_args,
                f"Argument --{arg.replace('_', '-')} not found in command",
            )

    def test_theme_options_match_readme(self):
        """Test that theme options match README"""
        from argparse import ArgumentParser

        parser = ArgumentParser()
        self.command.add_arguments(parser)

        theme_action = None
        for action in parser._actions:
            if hasattr(action, "dest") and action.dest == "theme":
                theme_action = action
                break

        self.assertIsNotNone(theme_action)
        if theme_action and hasattr(theme_action, "choices") and theme_action.choices:
            self.assertEqual(
                set(theme_action.choices), {"default", "dark", "minimal", "rainbow"}
            )

    def test_notification_platforms_match_readme(self):
        """Test that notification platforms match README"""
        from argparse import ArgumentParser

        parser = ArgumentParser()
        self.command.add_arguments(parser)

        notify_action = None
        for action in parser._actions:
            if hasattr(action, "dest") and action.dest == "notify":
                notify_action = action
                break

        self.assertIsNotNone(notify_action)
        if (
            notify_action
            and hasattr(notify_action, "choices")
            and notify_action.choices
        ):
            self.assertEqual(
                set(notify_action.choices), {"slack", "email", "discord", "teams"}
            )


if __name__ == "__main__":
    import django
    from django.test.utils import get_runner
    from django.conf import settings

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
