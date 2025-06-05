import time
from io import StringIO
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.management.base import OutputWrapper
from django_migrate_fresh.management.commands.migrate_fresh import Command


class PerformanceOptimizationTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)

    def test_performance_mode_initialization(self):
        """Test performance mode initialization"""
        options = {"performance": True}
        self.command._initialize_options(options)

        self.assertTrue(self.command.performance_mode)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_intelligent_table_dropping_postgresql_batch(self, mock_connection):
        """Test intelligent table dropping with batching for PostgreSQL"""
        self.command.performance_mode = True
        self.command.verbose = True

        mock_connection.vendor = "postgresql"
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock large number of tables to trigger batching
        tables = [f"table_{i}" for i in range(25)]

        with patch.object(self.command, "_get_table_list", return_value=tables):
            self.command._drop_all_tables()

            # Should execute multiple batch commands
            self.assertGreater(mock_cursor.execute.call_count, 1)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_intelligent_table_dropping_mysql_performance(self, mock_connection):
        """Test intelligent table dropping for MySQL in performance mode"""
        self.command.performance_mode = True
        self.command.verbose = True

        mock_connection.vendor = "mysql"
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        tables = ["table1", "table2", "table3"]

        with patch.object(self.command, "_get_table_list", return_value=tables):
            self.command._drop_all_tables()

            # Should use single DROP statement for performance
            execute_calls = mock_cursor.execute.call_args_list

            # Check for foreign key management and batch drop
            self.assertTrue(
                any("FOREIGN_KEY_CHECKS" in str(call) for call in execute_calls)
            )

    def test_benchmark_connection_timing(self):
        """Test connection benchmarking accuracy"""
        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.connection"
        ) as mock_connection:
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

            # Mock a slight delay
            def mock_execute(query):
                time.sleep(0.001)  # 1ms delay

            mock_cursor.execute.side_effect = mock_execute

            result = self.command._benchmark_connection()

            self.assertTrue(result.endswith("ms"))
            # Should measure some time > 0
            time_value = float(result[:-2])
            self.assertGreater(time_value, 0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_profiling_start_stop(self, mock_psutil):
        """Test profiling start and stop functionality"""
        mock_process = MagicMock()
        mock_process.memory_info.return_value.rss = 100 * 1024 * 1024  # 100MB
        mock_psutil.Process.return_value = mock_process

        # Start profiling
        self.command._start_profiling()

        self.assertTrue(hasattr(self.command, "profile_start_time"))
        self.assertTrue(hasattr(self.command, "profile_start_memory"))

        # Mock increased memory usage
        mock_process.memory_info.return_value.rss = 120 * 1024 * 1024  # 120MB

        # Stop profiling
        self.command._stop_profiling()

        output = self.out.getvalue()
        self.assertIn("Profile:", output)
        self.assertIn("Memory:", output)

    def test_profiling_without_psutil(self):
        """Test profiling gracefully handles missing psutil"""
        with patch(
            "django_migrate_fresh.management.commands.migrate_fresh.psutil", None
        ):
            # Should not crash
            self.command._start_profiling()
            self.command._stop_profiling()

    @patch("django_migrate_fresh.management.commands.migrate_fresh.call_command")
    def test_run_benchmarks_verbose(self, mock_call_command):
        """Test benchmark execution in verbose mode"""
        self.command.verbose = True

        with patch.object(self.command, "_benchmark_connection", return_value="5.2ms"):
            self.command._run_benchmarks()

            output = self.out.getvalue()
            self.assertIn("Running benchmarks", output)
            self.assertIn("Connection: 5.2ms", output)

    def test_run_benchmarks_non_verbose(self):
        """Test benchmark skipping in non-verbose mode"""
        self.command.verbose = False

        self.command._run_benchmarks()

        output = self.out.getvalue()
        self.assertEqual(output, "")  # No output in non-verbose mode

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_auto_optimize_database_postgresql(self, mock_connection):
        """Test database auto-optimization for PostgreSQL"""
        self.command.verbose = True
        mock_connection.vendor = "postgresql"
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        self.command._auto_optimize_database()

        mock_cursor.execute.assert_called_with("ANALYZE;")
        output = self.out.getvalue()
        self.assertIn("PostgreSQL statistics updated", output)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_auto_optimize_database_mysql(self, mock_connection):
        """Test database auto-optimization for MySQL"""
        self.command.verbose = True
        mock_connection.vendor = "mysql"

        self.command._auto_optimize_database()

        output = self.out.getvalue()
        self.assertIn("MySQL optimization completed", output)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.connection")
    def test_auto_optimize_database_sqlite(self, mock_connection):
        """Test database auto-optimization for SQLite"""
        self.command.verbose = True
        mock_connection.vendor = "sqlite"
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        self.command._auto_optimize_database()

        mock_cursor.execute.assert_called_with("ANALYZE;")
        output = self.out.getvalue()
        self.assertIn("SQLite optimization completed", output)


class CacheFeatureTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)

    def test_cache_enabled_flag(self):
        """Test cache enabled flag"""
        options = {"cache": True}
        self.command._initialize_options(options)

        self.assertTrue(self.command.cache_enabled)

    def test_cache_disabled_by_default(self):
        """Test cache is disabled by default"""
        options = {}
        self.command._initialize_options(options)

        self.assertFalse(self.command.cache_enabled)


class ParallelProcessingTestCase(TestCase):
    def setUp(self):
        self.command = Command()
        self.out = StringIO()
        self.command.stdout = OutputWrapper(self.out)

    def test_parallel_flag_initialization(self):
        """Test parallel processing flag initialization"""
        options = {"parallel": True}
        self.command._initialize_options(options)

        self.assertTrue(self.command.parallel)

    def test_parallel_workflow_selection(self):
        """Test parallel vs sequential workflow selection"""
        # Initialize required attributes
        self.command.parallel = True
        self.command.ai_mode = False
        self.command.benchmark = False

        # Mock steps
        steps = [
            ("Step 1", lambda: None, [], 1),
            ("Step 2", lambda: None, [], 1),
            ("Step 3", lambda: None, [], 1),
        ]

        with patch.object(
            self.command, "_execute_parallel_workflow"
        ) as mock_parallel, patch.object(
            self.command, "_execute_sequential_workflow"
        ) as mock_sequential, patch.object(
            self.command, "_get_enhanced_migration_steps", return_value=steps
        ), patch.object(
            self.command, "_execute_post_migration_tasks"
        ):

            self.command._execute_migration_workflow({}, time.time())

            # Should call parallel workflow for > 2 steps
            mock_parallel.assert_called_once()
            mock_sequential.assert_not_called()

    def test_sequential_workflow_fallback(self):
        """Test fallback to sequential workflow"""
        # Initialize required attributes
        self.command.parallel = False
        self.command.ai_mode = False
        self.command.benchmark = False

        steps = [("Step 1", lambda: None, [], 1)]

        with patch.object(
            self.command, "_execute_parallel_workflow"
        ) as mock_parallel, patch.object(
            self.command, "_execute_sequential_workflow"
        ) as mock_sequential, patch.object(
            self.command, "_get_enhanced_migration_steps", return_value=steps
        ), patch.object(
            self.command, "_execute_post_migration_tasks"
        ):

            self.command._execute_migration_workflow({}, time.time())

            # Should call sequential workflow
            mock_sequential.assert_called_once()
            mock_parallel.assert_not_called()


class SystemResourceTestCase(TestCase):
    def setUp(self):
        self.command = Command()

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_system_performance_factor_high_end(self, mock_psutil):
        """Test system performance factor for high-end system"""
        mock_psutil.cpu_count.return_value = 16  # High-end CPU
        mock_psutil.virtual_memory.return_value.total = 32 * 1024**3  # 32GB RAM

        factor = self.command._get_system_performance_factor()

        # Should return high performance factor (capped at 2.0)
        self.assertEqual(factor, 2.0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_system_performance_factor_low_end(self, mock_psutil):
        """Test system performance factor for low-end system"""
        mock_psutil.cpu_count.return_value = 2  # Low-end CPU
        mock_psutil.virtual_memory.return_value.total = 4 * 1024**3  # 4GB RAM

        factor = self.command._get_system_performance_factor()

        # Should return lower performance factor
        self.assertLess(factor, 1.0)

    @patch("django_migrate_fresh.management.commands.migrate_fresh.psutil")
    def test_system_performance_factor_null_cpu(self, mock_psutil):
        """Test system performance factor with null CPU count"""
        mock_psutil.cpu_count.return_value = None  # CPU count unavailable
        mock_psutil.virtual_memory.return_value.total = 8 * 1024**3  # 8GB RAM

        factor = self.command._get_system_performance_factor()

        # Should handle null CPU count gracefully
        self.assertIsInstance(factor, float)
        self.assertGreater(factor, 0)


if __name__ == "__main__":
    import django
    from django.test.utils import get_runner
    from django.conf import settings

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests.test_performance_features"])
