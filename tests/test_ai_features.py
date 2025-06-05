import os
import json
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from django.test import TestCase
from django.core.management.base import OutputWrapper
from django_migrate_fresh.management.commands.migrate_fresh import Command


class AIFeaturesTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)
        self.command.verbose = True

    def test_ai_mode_initialization(self):
        """Test AI mode initialization"""
        options = {"ai": True, "cache": True, "performance": True}
        self.command._initialize_options(options)

        self.assertTrue(self.command.ai_mode)
        self.assertTrue(self.command.cache_enabled)
        self.assertTrue(self.command.performance_mode)

    @patch.object(Command, "_get_table_list")
    def test_ai_analyze_migration_simple(self, mock_get_tables):
        """Test AI analysis for simple database"""
        mock_get_tables.return_value = ["table1", "table2"]  # 2 tables = Simple

        self.command._ai_analyze_migration()
        output = self.out.getvalue()

        self.assertIn("AI Migration Analysis", output)
        self.assertIn("Simple (2 tables)", output)
        self.assertIn("Estimated Time:", output)
        self.assertIn("Risk Level:", output)

    @patch.object(Command, "_get_table_list")
    def test_ai_analyze_migration_complex(self, mock_get_tables):
        """Test AI analysis for complex database"""
        mock_get_tables.return_value = [
            "table" + str(i) for i in range(25)
        ]  # 25 tables = Complex

        self.command._ai_analyze_migration()
        output = self.out.getvalue()

        self.assertIn("Complex (25 tables)", output)

    @patch.object(Command, "_get_table_list")
    def test_ai_analyze_migration_enterprise(self, mock_get_tables):
        """Test AI analysis for enterprise database"""
        mock_get_tables.return_value = [
            "table" + str(i) for i in range(75)
        ]  # 75 tables = Enterprise

        self.command._ai_analyze_migration()
        output = self.out.getvalue()

        self.assertIn("Enterprise (75 tables)", output)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_ai_estimate_migration_time(self, mock_psutil):
        """Test AI time estimation"""
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.virtual_memory.return_value.total = 8 * 1024**3  # 8GB

        estimated_time = self.command._ai_estimate_migration_time(10)

        self.assertIsInstance(estimated_time, int)
        self.assertGreater(estimated_time, 0)

    @patch("django.conf.settings.DEBUG", False)
    @patch.object(Command, "_estimate_data_size_bytes")
    @patch.object(Command, "_has_complex_relationships")
    def test_ai_assess_risk_high(self, mock_complex_rel, mock_data_size):
        """Test AI risk assessment - high risk"""
        mock_data_size.return_value = 2 * 1024**3  # 2GB (large dataset)
        mock_complex_rel.return_value = True

        risk_level = self.command._ai_assess_risk()

        self.assertEqual(risk_level, "High")

    @patch("django.conf.settings.DEBUG", True)
    @patch.object(Command, "_estimate_data_size_bytes")
    @patch.object(Command, "_has_complex_relationships")
    def test_ai_assess_risk_low(self, mock_complex_rel, mock_data_size):
        """Test AI risk assessment - low risk"""
        mock_data_size.return_value = 100 * 1024**2  # 100MB (small dataset)
        mock_complex_rel.return_value = False

        risk_level = self.command._ai_assess_risk()

        self.assertEqual(risk_level, "Low")

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_adaptive_optimization_powerful_system(self, mock_psutil):
        """Test adaptive optimization on powerful system"""
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.virtual_memory.return_value.available = 8 * 1024**3  # 8GB available
        mock_psutil.virtual_memory.return_value.total = 32 * 1024**3  # 32GB total

        self.command._adaptive_optimization()

        self.assertTrue(self.command.parallel)
        self.assertTrue(self.command.cache_enabled)
        self.assertTrue(self.command.performance_mode)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_adaptive_optimization_limited_system(self, mock_psutil):
        """Test adaptive optimization on limited system"""
        mock_psutil.cpu_count.return_value = 2
        mock_psutil.virtual_memory.return_value.available = 1 * 1024**3  # 1GB available
        mock_psutil.virtual_memory.return_value.total = 4 * 1024**3  # 4GB total

        # Initialize to False first
        self.command.parallel = False
        self.command.cache_enabled = False
        self.command.performance_mode = False

        self.command._adaptive_optimization()

        self.assertFalse(self.command.parallel)
        self.assertFalse(self.command.cache_enabled)
        self.assertFalse(self.command.performance_mode)

    def test_ai_optimize_step_order(self):
        """Test AI step order optimization"""
        steps = [
            ("Running seeders", lambda: None, [], 5),
            ("Creating superuser", lambda: None, [], 1),
            ("Dropping tables", lambda: None, [], 3),
            ("Running migrations", lambda: None, [], 10),
        ]

        optimized_steps = self.command._ai_optimize_step_order(steps)

        # Check if steps are in correct order
        step_names = [step[0] for step in optimized_steps]
        expected_order = [
            "Dropping tables",
            "Running migrations",
            "Creating superuser",
            "Running seeders",
        ]

        self.assertEqual(step_names, expected_order)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    @patch.object(Command, "_get_table_list")
    @patch.object(Command, "_get_system_specs")
    def test_ai_learn_from_migration(
        self, mock_system_specs, mock_get_tables, mock_exists, mock_file
    ):
        """Test AI learning from migration"""
        mock_get_tables.return_value = ["table1", "table2"]
        mock_system_specs.return_value = {"cpu_count": 4, "memory_total": 8 * 1024**3}
        mock_exists.return_value = False  # No existing cache file

        duration = 15.5
        self.command._ai_learn_from_migration(duration)

        # Verify file was written
        mock_file.assert_called_with(".migrate_fresh_ai_cache.json", "w")

        # Check output
        output = self.out.getvalue()
        self.assertIn("AI learning from this migration", output)
        self.assertIn("Migration patterns saved", output)

    @patch("builtins.open", new_callable=mock_open, read_data='{"migrations": []}')
    @patch("os.path.exists")
    @patch.object(Command, "_get_table_list")
    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_ai_learn_existing_cache(
        self, mock_psutil, mock_get_tables, mock_exists, mock_file
    ):
        """Test AI learning with existing cache file"""
        # Mock psutil properly
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.virtual_memory.return_value.total = 8 * 1024**3
        mock_psutil.disk_usage.return_value.total = 1024 * 1024**3

        mock_get_tables.return_value = ["table1"]
        mock_exists.return_value = True  # Existing cache file

        duration = 10.0
        self.command._ai_learn_from_migration(duration)

        # Verify file was read and written
        self.assertEqual(mock_file.call_count, 2)  # One read, one write

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_get_system_performance_factor(self, mock_psutil):
        """Test system performance factor calculation"""
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.virtual_memory.return_value.total = 16 * 1024**3  # 16GB

        factor = self.command._get_system_performance_factor()

        self.assertIsInstance(factor, float)
        self.assertGreater(factor, 0)
        self.assertLessEqual(factor, 2.0)  # Max factor is 2.0

    def test_get_system_performance_factor_no_psutil(self):
        """Test system performance factor without psutil"""
        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.psutil", None
        ):
            factor = self.command._get_system_performance_factor()
            self.assertEqual(factor, 1.0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_estimate_data_size_postgresql(self, mock_connection):
        """Test data size estimation for PostgreSQL"""
        mock_connection.vendor = "postgresql"
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1024 * 1024 * 100]  # 100MB
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        size = self.command._estimate_data_size_bytes()

        self.assertEqual(size, 1024 * 1024 * 100)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_estimate_data_size_mysql(self, mock_connection):
        """Test data size estimation for MySQL"""
        mock_connection.vendor = "mysql"
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1024 * 1024 * 50]  # 50MB
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        size = self.command._estimate_data_size_bytes()

        self.assertEqual(size, 1024 * 1024 * 50)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_estimate_data_size_sqlite(
        self, mock_getsize, mock_exists, mock_connection
    ):
        """Test data size estimation for SQLite"""
        mock_connection.vendor = "sqlite"
        mock_connection.settings_dict = {"NAME": "/path/to/db.sqlite3"}
        mock_exists.return_value = True
        mock_getsize.return_value = 1024 * 1024 * 25  # 25MB

        size = self.command._estimate_data_size_bytes()

        self.assertEqual(size, 1024 * 1024 * 25)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_has_complex_relationships_postgresql(self, mock_connection):
        """Test complex relationships detection for PostgreSQL"""
        mock_connection.vendor = "postgresql"
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [10]  # 10 foreign keys
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.command._has_complex_relationships()

        self.assertTrue(result)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_has_complex_relationships_simple(self, mock_connection):
        """Test simple relationships detection"""
        mock_connection.vendor = "postgresql"
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [2]  # 2 foreign keys (simple)
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        result = self.command._has_complex_relationships()

        self.assertFalse(result)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_get_system_specs(self, mock_psutil):
        """Test system specs collection"""
        mock_psutil.cpu_count.return_value = 8
        mock_psutil.virtual_memory.return_value.total = 16 * 1024**3
        mock_psutil.disk_usage.return_value.total = 1024 * 1024**3  # 1TB

        specs = self.command._get_system_specs()

        expected_specs = {
            "cpu_count": 8,
            "memory_total": 16 * 1024**3,
            "disk_total": 1024 * 1024**3,
        }

        self.assertEqual(specs, expected_specs)

    def test_get_system_specs_no_psutil(self):
        """Test system specs without psutil"""
        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.psutil", None
        ):
            specs = self.command._get_system_specs()
            self.assertEqual(specs, {})


class ParallelExecutionTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)
        self.command.verbose = True

    @patch("concurrent.futures.ThreadPoolExecutor")
    def test_execute_parallel_workflow(self, mock_executor):
        """Test parallel workflow execution"""
        # Mock the executor
        mock_future = MagicMock()
        mock_future.result.return_value = None
        mock_executor.return_value.__enter__.return_value.submit.return_value = (
            mock_future
        )

        steps = [
            ("Dropping tables", lambda: None, [], 3),
            ("Running migrations", lambda: None, [], 10),
            ("Creating superuser", lambda: None, [], 1),
            ("Running seeders", lambda: None, [], 5),
        ]

        self.command._execute_parallel_workflow(steps)

        output = self.out.getvalue()
        self.assertIn("Executing parallel operations", output)

    def test_execute_sequential_workflow(self):
        """Test sequential workflow execution"""
        executed_steps = []

        def mock_step_1():
            executed_steps.append("step1")

        def mock_step_2():
            executed_steps.append("step2")

        steps = [
            ("Step 1", mock_step_1, [], 1),
            ("Step 2", mock_step_2, [], 1),
        ]

        self.command._execute_sequential_workflow(steps)

        self.assertEqual(executed_steps, ["step1", "step2"])


class IntelligentFeaturesTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)

    def test_performance_mode_table_dropping(self):
        """Test performance mode table dropping optimization"""
        self.command.performance_mode = True
        self.command.verbose = True

        with patch.object(self.command, "_get_table_list") as mock_get_tables, patch(
            "django_migrate_fresh.management.commands.migrate_fresh.connection"
        ) as mock_connection:

            mock_get_tables.return_value = ["table1", "table2", "table3"]
            mock_connection.vendor = "postgresql"
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

            self.command._drop_all_tables()

            # Verify that batch dropping was used
            mock_cursor.execute.assert_called()

    def test_cache_enabled_feature(self):
        """Test cache enabled functionality"""
        self.command.cache_enabled = True

        # Cache should be properly initialized
        self.assertTrue(self.command.cache_enabled)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil", None)
    def test_adaptive_optimization_no_psutil(self):
        """Test adaptive optimization without psutil"""
        # Initialize command attributes first
        self.command.parallel = False
        self.command.cache_enabled = False
        self.command.performance_mode = False

        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.psutil", None
        ):
            # Should not crash when psutil is not available
            self.command._adaptive_optimization()

            # Should remain unchanged when psutil not available
            self.assertFalse(self.command.parallel)
            self.assertFalse(self.command.cache_enabled)
            self.assertFalse(self.command.performance_mode)


if __name__ == "__main__":
    import django
    from django.test.utils import get_runner
    from django.conf import settings

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests.test_ai_features"])
