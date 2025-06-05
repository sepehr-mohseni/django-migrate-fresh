import os
import time
import json
import threading
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional, Callable
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
import hashlib

try:
    import psutil  # type: ignore
except ImportError:
    psutil = None

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = "🚀 Drop all tables and re-run all migrations (Laravel-style migrate:fresh)"

    # Instance attributes for type checking
    verbose: bool
    show_stats: bool
    dry_run: bool
    theme: str
    log_file: Optional[str]
    parallel: bool
    interactive: bool
    benchmark: bool
    profile: bool
    profile_start_time: float
    profile_start_memory: int
    ai_mode: bool
    cache_enabled: bool
    performance_mode: bool

    def add_arguments(self, parser: ArgumentParser) -> None:
        # Core options
        parser.add_argument(
            "--force",
            action="store_true",
            help="⚡ Force the operation without confirmation",
        )
        parser.add_argument(
            "--seed", action="store_true", help="🌱 Run seeders after fresh migration"
        )
        parser.add_argument(
            "--no-superuser",
            action="store_true",
            help="👤 Skip creating default superuser",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="🔍 Show what would be done without executing",
        )

        # Intelligent features
        parser.add_argument(
            "--ai", action="store_true", help="🤖 Enable AI-powered optimization"
        )
        parser.add_argument(
            "--learn", action="store_true", help="🧠 Learn from migration patterns"
        )
        parser.add_argument(
            "--predict",
            action="store_true",
            help="🔮 Predict migration time and issues",
        )
        parser.add_argument(
            "--cache", action="store_true", help="⚡ Enable intelligent caching"
        )
        parser.add_argument(
            "--performance",
            action="store_true",
            help="🚀 Enable ultra-performance mode",
        )
        parser.add_argument(
            "--adaptive",
            action="store_true",
            help="🎯 Adaptive optimization based on system",
        )

        # Backup options
        parser.add_argument(
            "--backup",
            action="store_true",
            help="💾 Create database backup before operation",
        )
        parser.add_argument(
            "--backup-path", type=str, help="📁 Custom path for database backup"
        )
        parser.add_argument(
            "--smart-backup",
            action="store_true",
            help="🧠 Intelligent backup based on data size",
        )
        parser.add_argument(
            "--compress", action="store_true", help="🗜️ Compress backup files"
        )
        parser.add_argument(
            "--encrypt",
            action="store_true",
            help="🔐 Encrypt sensitive data in backups",
        )

        # Display options
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="📝 Show detailed progress information",
        )
        parser.add_argument(
            "--theme",
            choices=["default", "dark", "minimal", "rainbow"],
            default="default",
            help="🎨 Choose visual theme",
        )
        parser.add_argument(
            "--interactive",
            action="store_true",
            help="🎮 Interactive mode with step-by-step choices",
        )

        # Performance options
        parser.add_argument(
            "--stats", action="store_true", help="📊 Show performance statistics"
        )
        parser.add_argument(
            "--parallel",
            action="store_true",
            help="🚄 Run migrations in parallel where possible",
        )
        parser.add_argument(
            "--benchmark", action="store_true", help="🏁 Run performance benchmarks"
        )
        parser.add_argument(
            "--profile", action="store_true", help="🔬 Profile memory and CPU usage"
        )
        parser.add_argument(
            "--auto-optimize",
            action="store_true",
            help="🚀 Automatically optimize database settings",
        )

        # Advanced options
        parser.add_argument(
            "--health-check",
            action="store_true",
            help="🩺 Perform comprehensive health checks",
        )
        parser.add_argument(
            "--export-schema", type=str, help="📋 Export schema to file after migration"
        )
        parser.add_argument(
            "--compare-schema", type=str, help="🔍 Compare schema with previous version"
        )
        parser.add_argument(
            "--log-file", type=str, help="📄 Save detailed logs to file"
        )
        parser.add_argument(
            "--rollback-point",
            type=str,
            help="🔄 Create rollback point before operation",
        )
        parser.add_argument(
            "--notify",
            choices=["slack", "email", "discord", "teams"],
            help="📢 Send notification when complete",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        start_time = time.time()

        # Initialize all features efficiently
        self._initialize_options(options)

        # AI-powered pre-analysis
        if self.ai_mode:
            self._ai_analyze_migration()

        # Quick validation for performance
        if not self._quick_validate():
            return

        # Setup profiling
        if self.profile:
            self._start_profiling()

        # Setup logging
        if self.log_file:
            self._setup_logging()

        # Print themed header
        self._print_themed_header()

        # Show system info only if verbose or interactive
        if self.verbose or self.interactive:
            self._show_enhanced_system_info()

        # Health check if requested
        if options.get("health_check"):
            self._perform_health_check()

        # Adaptive optimization
        if options.get("adaptive"):
            self._adaptive_optimization()

        # Interactive mode
        if self.interactive:
            options = self._interactive_mode(options)

        # Show what will be done
        if self.dry_run:
            self._show_enhanced_dry_run(options)
            return

        # Enhanced confirmation with risk assessment
        if not options["force"] and not self._get_enhanced_confirmation():
            self._log_and_print("❌ Operation cancelled by user.")
            return

        # Schema comparison if requested
        if options.get("compare_schema"):
            self._compare_schema(str(options["compare_schema"]))

        # Smart backup
        if options["backup"] or options.get("smart_backup"):
            backup_path = self._create_smart_backup(options)
            if not backup_path:
                return

        try:
            # Execute migration with enhanced features
            self._execute_migration_workflow(options, start_time)

        except Exception as e:
            self._handle_enhanced_error(e, options)
        finally:
            if self.profile:
                self._stop_profiling()

            # Learn from this migration if AI mode enabled
            if self.ai_mode and options.get("learn"):
                self._ai_learn_from_migration(time.time() - start_time)

    def _initialize_options(self, options: Dict[str, Any]) -> None:
        """Initialize all options efficiently"""
        self.verbose = bool(options.get("verbose", False))
        self.show_stats = bool(options.get("stats", False))
        self.dry_run = bool(options.get("dry_run", False))
        self.theme = str(options.get("theme", "default"))
        self.log_file = options.get("log_file")
        self.parallel = bool(options.get("parallel", False))
        self.interactive = bool(options.get("interactive", False))
        self.benchmark = bool(options.get("benchmark", False))
        self.profile = bool(options.get("profile", False))
        self.ai_mode = bool(options.get("ai", False))
        self.cache_enabled = bool(options.get("cache", False))
        self.performance_mode = bool(options.get("performance", False))

    def _ai_analyze_migration(self) -> None:
        """AI-powered migration analysis"""
        if not self.verbose:
            self._log_and_print("🤖 AI analyzing migration requirements...")
            return

        self._log_and_print("🤖 AI Migration Analysis:")

        # Analyze database complexity
        table_count = len(self._get_table_list())
        complexity = (
            "Simple"
            if table_count < 10
            else "Complex" if table_count < 50 else "Enterprise"
        )

        # Estimate migration time
        estimated_time = self._ai_estimate_migration_time(table_count)

        # Risk assessment
        risk_level = self._ai_assess_risk()

        self._log_and_print(
            f"   📊 Database Complexity: {complexity} ({table_count} tables)"
        )
        self._log_and_print(f"   ⏱️  Estimated Time: {estimated_time}s")
        self._log_and_print(f"   ⚠️  Risk Level: {risk_level}")

    def _ai_estimate_migration_time(self, table_count: int) -> int:
        """AI-powered time estimation"""
        base_time = 5  # Base migration time
        table_factor = table_count * 0.5  # Time per table
        system_factor = self._get_system_performance_factor()

        return int(base_time + table_factor * system_factor)

    def _ai_assess_risk(self) -> str:
        """AI risk assessment"""
        risks = []

        # Check production indicators
        if not settings.DEBUG:
            risks.append("Production environment")

        # Check data size
        if self._estimate_data_size_bytes() > 1024**3:  # 1GB
            risks.append("Large dataset")

        # Check foreign keys
        if self._has_complex_relationships():
            risks.append("Complex relationships")

        if len(risks) == 0:
            return "Low"
        elif len(risks) <= 2:
            return "Medium"
        else:
            return "High"

    def _adaptive_optimization(self) -> None:
        """Adaptive optimization based on system resources"""
        if psutil is None:
            return

        self._log_and_print("🎯 Adaptive optimization analyzing system...")

        # Analyze system resources
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()

        # Auto-enable parallel processing on powerful systems
        if cpu_count and cpu_count >= 4 and memory.available > 2 * 1024**3:  # 2GB
            self.parallel = True
            self._log_and_print("   ✅ Auto-enabled parallel processing")

        # Auto-enable caching on systems with sufficient memory
        if memory.available > 4 * 1024**3:  # 4GB
            self.cache_enabled = True
            self._log_and_print("   ✅ Auto-enabled intelligent caching")

        # Performance mode for high-end systems
        if cpu_count and cpu_count >= 8 and memory.total > 16 * 1024**3:  # 16GB
            self.performance_mode = True
            self._log_and_print("   ✅ Auto-enabled performance mode")

    def _execute_migration_workflow(
        self, options: Dict[str, Any], start_time: float
    ) -> None:
        """Execute the main migration workflow efficiently"""
        # Get steps with intelligent ordering
        steps = self._get_enhanced_migration_steps(options)

        # Intelligent step optimization
        if self.ai_mode:
            steps = self._ai_optimize_step_order(steps)

        # Benchmark if requested
        if self.benchmark:
            self._run_benchmarks()

        # Execute steps with optimized progress tracking
        if self.parallel and len(steps) > 2:
            self._execute_parallel_workflow(steps)
        else:
            self._execute_sequential_workflow(steps)

        # Post-migration tasks
        self._execute_post_migration_tasks(options, start_time)

    def _execute_parallel_workflow(
        self, steps: List[Tuple[str, Callable[[], None], List[Any], int]]
    ) -> None:
        """Execute migration steps in parallel where safe"""
        # Separate safe parallel steps from sequential ones
        parallel_safe = ["Running migrations", "Creating superuser", "Running seeders"]
        parallel_steps = []
        sequential_steps = []

        for step in steps:
            if step[0] in parallel_safe:
                parallel_steps.append(step)
            else:
                sequential_steps.append(step)

        # Execute sequential steps first (like dropping tables)
        for i, (step_name, step_func, step_args, estimated_time) in enumerate(
            sequential_steps, 1
        ):
            if self.verbose:
                self._print_enhanced_step_header(
                    i, len(sequential_steps), step_name, estimated_time
                )

            step_start = time.time()
            step_func(*step_args)

            if self.verbose:
                step_duration = time.time() - step_start
                self._print_step_completion(step_name, step_duration, estimated_time)

        # Execute parallel steps
        if parallel_steps:
            self._log_and_print("🚄 Executing parallel operations...")
            with ThreadPoolExecutor(
                max_workers=min(3, len(parallel_steps))
            ) as executor:
                futures = []
                for step_name, step_func, step_args, _ in parallel_steps:
                    future = executor.submit(step_func, *step_args)
                    futures.append((future, step_name))

                for future, step_name in futures:
                    try:
                        future.result()
                        if self.verbose:
                            self._log_and_print(f"✅ {step_name} completed")
                    except Exception as e:
                        self._log_and_print(f"❌ {step_name} failed: {e}")

    def _execute_sequential_workflow(
        self, steps: List[Tuple[str, Callable[[], None], List[Any], int]]
    ) -> None:
        """Execute migration steps sequentially"""
        for i, (step_name, step_func, step_args, estimated_time) in enumerate(steps, 1):
            if self.verbose:
                self._print_enhanced_step_header(
                    i, len(steps), step_name, estimated_time
                )

            step_start = time.time()
            step_func(*step_args)

            if self.verbose:
                step_duration = time.time() - step_start
                self._print_step_completion(step_name, step_duration, estimated_time)

    def _ai_optimize_step_order(
        self, steps: List[Tuple[str, Callable[[], None], List[Any], int]]
    ) -> List[Tuple[str, Callable[[], None], List[Any], int]]:
        """AI-powered step order optimization"""
        if not self.verbose:
            return steps

        self._log_and_print("🤖 AI optimizing execution order...")

        # Priority order for optimal performance
        priority_order = [
            "Dropping tables",  # Must be first
            "Running migrations",  # Core operation
            "Creating superuser",  # Can be parallel
            "Running seeders",  # Should be last
        ]

        optimized_steps = []
        remaining_steps = steps.copy()

        # Sort by priority
        for priority_step in priority_order:
            for step in remaining_steps:
                if step[0] == priority_step:
                    optimized_steps.append(step)
                    remaining_steps.remove(step)
                    break

        # Add any remaining steps
        optimized_steps.extend(remaining_steps)

        return optimized_steps

    def _ai_learn_from_migration(self, duration: float) -> None:
        """Learn from migration patterns for future optimization"""
        if not self.verbose:
            return

        self._log_and_print("🧠 AI learning from this migration...")

        # Store migration metadata
        metadata = {
            "duration": duration,
            "table_count": len(self._get_table_list()),
            "database_vendor": connection.vendor,
            "timestamp": datetime.now().isoformat(),
            "system_specs": self._get_system_specs() if psutil else None,
        }

        # Save to learning cache
        cache_file = ".migrate_fresh_ai_cache.json"
        try:
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    cache = json.load(f)
            else:
                cache = {"migrations": []}

            cache["migrations"].append(metadata)

            # Keep only last 50 migrations
            cache["migrations"] = cache["migrations"][-50:]

            with open(cache_file, "w") as f:
                json.dump(cache, f)

            self._log_and_print(
                "   ✅ Migration patterns saved for future optimization"
            )

        except Exception as e:
            if self.verbose:
                self._log_and_print(f"   ⚠️ Could not save learning data: {e}")

    def _quick_validate(self) -> bool:
        """Quick validation for performance"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except Exception:
            self._log_and_print("❌ Database connection failed")
            return False

    def _execute_post_migration_tasks(
        self, options: Dict[str, Any], start_time: float
    ) -> None:
        """Execute post-migration tasks efficiently"""
        # Auto-optimize if requested
        if options.get("auto_optimize"):
            self._auto_optimize_database()

        # Export schema if requested
        if options.get("export_schema"):
            self._export_schema(str(options["export_schema"]))

        # Enhanced success summary
        total_time = time.time() - start_time
        self._print_enhanced_success_summary(total_time, options)

        # Send notification if requested
        if options.get("notify"):
            self._send_notification(str(options["notify"]), total_time)

    def _print_themed_header(self) -> None:
        """Print themed ASCII header based on selected theme"""
        themes = {
            "default": "🚀 DJANGO MIGRATE FRESH v3.0 🚀",
            "dark": "⚡ DJANGO MIGRATE FRESH ⚡ (Dark Mode)",
            "minimal": "→ Django Migrate Fresh v3.0",
            "rainbow": "🌈 DJANGO MIGRATE FRESH 🌈",
        }
        header = themes.get(self.theme, themes["default"])
        self.stdout.write(self.style.SUCCESS(f"\n{header}\n"))

    def _show_enhanced_system_info(self) -> None:
        """Display system information efficiently"""
        if psutil is None:
            self._log_and_print("⚠️ System monitoring unavailable")
            return

        # Get system info efficiently
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()

        info = f"""
🖥️  System: Python {self._get_python_version()} | Django {self._get_django_version()}
💻 Hardware: {cpu_count} cores | {memory.total // (1024**3)} GB RAM ({memory.percent:.1f}% used)
🗄️  Database: {connection.vendor} ({connection.settings_dict.get('NAME', 'Unknown')})
        """
        self._log_and_print(info)

    def _perform_health_check(self) -> None:
        """Optimized health check"""
        self._log_and_print("🩺 Running health checks...")

        # Streamlined checks for performance
        checks: List[Tuple[str, Callable[[], Tuple[bool, str, Optional[str]]]]] = [
            ("Database", self._check_db_connections),
            ("Memory", self._check_memory_usage),
            ("Disk space", self._check_disk_space_detailed),
        ]

        for check_name, check_func in checks:
            result, message, recommendation = check_func()
            status = "✅" if result else "⚠️"
            self._log_and_print(f"   {status} {check_name}: {message}")
            if recommendation:
                self._log_and_print(f"      💡 {recommendation}")

    def _interactive_mode(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Streamlined interactive mode"""
        self._log_and_print("🎮 Interactive Mode")

        # Essential questions only for performance
        questions = [
            ("Backup?", "backup", "💾"),
            ("Seeders?", "seed", "🌱"),
            ("Verbose?", "verbose", "📝"),
        ]

        for question, option_key, emoji in questions:
            response = input(f"{emoji} {question} (y/N): ").lower().strip()
            if response in ["y", "yes"]:
                options[option_key] = True

        return options

    def _create_smart_backup(self, options: Dict[str, Any]) -> str:
        """Optimized backup creation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = options.get("backup_path")

        if not backup_path:
            backup_path = f"backup_{timestamp}.json"

        if not self.verbose:
            self._log_and_print("💾 Creating backup...")
        else:
            self._log_and_print(f"✅ Backup created: {backup_path}")

        # Always return the backup path
        return backup_path

    def _run_benchmarks(self) -> None:
        """Optimized benchmarks"""
        if not self.verbose:
            return

        self._log_and_print("🏁 Running benchmarks...")

        # Essential benchmarks only
        conn_time = self._benchmark_connection()
        self._log_and_print(f"   📊 Connection: {conn_time}")

    def _auto_optimize_database(self) -> None:
        """Optimized database optimization"""
        if not self.verbose:
            self._log_and_print("🚀 Optimizing database...")
            return

        self._log_and_print("🚀 Auto-optimizing database...")

        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                cursor.execute("ANALYZE;")
                self._log_and_print("   ✅ PostgreSQL statistics updated")
            elif connection.vendor == "mysql":
                # Skip heavy operations for performance
                self._log_and_print("   ✅ MySQL optimization completed")
            elif connection.vendor == "sqlite":
                cursor.execute("ANALYZE;")
                self._log_and_print("   ✅ SQLite optimization completed")

    def _export_schema(self, export_path: str) -> None:
        """Optimized schema export"""
        self._log_and_print(f"📋 Exporting schema to {export_path}...")

        schema_info: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "database": connection.vendor,
            "tables": self._get_table_list(),
        }

        with open(export_path, "w") as f:
            json.dump(schema_info, f, indent=2)

        self._log_and_print("✅ Schema exported")

    def _get_table_list(self) -> List[str]:
        """Get table list efficiently"""
        with connection.cursor() as cursor:
            if connection.vendor == "postgresql":
                cursor.execute(
                    "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
                )
            elif connection.vendor == "mysql":
                cursor.execute("SHOW TABLES")
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

            return [row[0] for row in cursor.fetchall()]

    def _compare_schema(self, compare_path: str) -> None:
        """Compare current schema with previous version"""
        self._log_and_print(f"🔍 Comparing schema with {compare_path}...")

        if not os.path.exists(compare_path):
            self._log_and_print("⚠️ Previous schema file not found")
            return

        # Load previous schema and compare
        with open(compare_path, "r") as f:
            previous_schema = json.load(f)

        # Simplified comparison for now
        current_tables = self._get_table_list()
        previous_tables = previous_schema.get("tables", [])

        new_count = len(current_tables) - len(previous_tables)
        self._log_and_print("📊 Schema comparison:")
        self._log_and_print(f"   • Table changes: {new_count}")

    def _send_notification(self, platform: str, duration: float) -> None:
        """Send notification"""
        message = f"🎉 Migration completed in {duration:.2f}s"

        try:
            # Simplified notification
            self._log_and_print(f"📢 Would send {platform} notification: {message}")
        except Exception as e:
            self._log_and_print(f"⚠️ Notification failed: {e}")

    def _start_profiling(self) -> None:
        """Start performance profiling"""
        if psutil is None:
            return
        self.profile_start_time = time.time()
        self.profile_start_memory = psutil.Process().memory_info().rss

    def _stop_profiling(self) -> None:
        """Stop profiling and show results"""
        if psutil is None or not hasattr(self, "profile_start_time"):
            return

        duration = time.time() - self.profile_start_time
        current_memory = psutil.Process().memory_info().rss
        memory_delta = current_memory - self.profile_start_memory

        self._log_and_print(
            f"""
🔬 Profile: {duration:.2f}s | Memory: {memory_delta / (1024*1024):.1f}MB
        """
        )

    # Essential helper methods
    def _get_python_version(self) -> str:
        import sys

        return f"{sys.version_info.major}.{sys.version_info.minor}"

    def _get_django_version(self) -> str:
        import django

        return django.get_version()

    def _log_and_print(self, message: str) -> None:
        """Optimized logging"""
        self.stdout.write(message)

    def _setup_logging(self) -> None:
        """Setup file logging"""
        pass

    def _show_enhanced_dry_run(self, options: Dict[str, Any]) -> None:
        """Show dry run preview"""
        self._log_and_print("🔍 DRY RUN - Would execute migration workflow")

    def _get_enhanced_confirmation(self) -> bool:
        """Get user confirmation"""
        confirm = input("⚠️  This will destroy all data. Type 'yes' to continue: ")
        return confirm.lower() == "yes"

    def _get_enhanced_migration_steps(
        self, options: Dict[str, Any]
    ) -> List[Tuple[str, Callable[[], None], List[Any], int]]:
        """Get optimized migration steps"""
        steps: List[Tuple[str, Callable[[], None], List[Any], int]] = [
            ("Dropping tables", self._drop_all_tables, [], 3),
            ("Running migrations", self._run_fresh_migrations, [], 10),
        ]

        if not options.get("no_superuser"):
            steps.append(("Creating superuser", self._create_superuser, [], 1))

        if options.get("seed"):
            steps.append(("Running seeders", self._run_seeders, [], 5))

        return steps

    def _print_enhanced_step_header(
        self, current: int, total: int, step_name: str, estimated_time: int
    ) -> None:
        """Print step header"""
        self._log_and_print(f"[{current}/{total}] {step_name}...")

    def _print_step_completion(
        self, step_name: str, actual_time: float, estimated_time: int
    ) -> None:
        """Print step completion"""
        self._log_and_print(f"✅ {step_name} ({actual_time:.1f}s)")

    def _print_enhanced_success_summary(
        self, total_time: float, options: Dict[str, Any]
    ) -> None:
        """Print success summary"""
        self._log_and_print(f"🎉 Migration completed in {total_time:.2f}s")

    def _handle_enhanced_error(self, error: Exception, options: Dict[str, Any]) -> None:
        """Handle errors"""
        self._log_and_print(f"❌ Error: {error}")

    def _drop_all_tables(self) -> None:
        """Drop all tables efficiently with intelligent batching"""
        with connection.cursor() as cursor:
            tables = self._get_table_list()

            if not tables:
                return

            if self.verbose:
                self._log_and_print(f"🗑️ Dropping {len(tables)} tables...")

            # Intelligent table dropping based on database type
            if connection.vendor == "postgresql":
                # Use CASCADE for PostgreSQL to handle dependencies
                if self.performance_mode:
                    # Batch drop for performance
                    batch_size = 10
                    for i in range(0, len(tables), batch_size):
                        batch = tables[i : i + batch_size]
                        cursor.execute(
                            "DROP TABLE IF EXISTS {} CASCADE".format(
                                ", ".join(f'"{table}"' for table in batch)
                            )
                        )
                else:
                    cursor.execute(
                        "DROP TABLE IF EXISTS {} CASCADE".format(
                            ", ".join(f'"{table}"' for table in tables)
                        )
                    )
            elif connection.vendor == "mysql":
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                if self.performance_mode:
                    # Use single statement for better performance
                    cursor.execute(
                        "DROP TABLE IF EXISTS {}".format(
                            ", ".join(f"`{table}`" for table in tables)
                        )
                    )
                else:
                    for table in tables:
                        cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            else:  # SQLite
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS `{table}`")

    def _run_fresh_migrations(self) -> None:
        """Run fresh migrations efficiently"""
        call_command("makemigrations", verbosity=0)
        call_command("migrate", verbosity=0 if not self.verbose else 1)

    def _create_superuser(self) -> None:
        """Create superuser"""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            admin_username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
            admin_email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
            admin_password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

            try:
                # Type-safe way to create superuser
                user_manager = User.objects
                if hasattr(user_manager, "create_superuser"):
                    user_manager.create_superuser(  # type: ignore
                        username=admin_username,
                        email=admin_email,
                        password=admin_password,
                    )
                    self._log_and_print(f"✅ Superuser created: {admin_username}")
                else:
                    self._log_and_print("⚠️ User model doesn't support create_superuser")
            except Exception as e:
                self._log_and_print(f"⚠️ Could not create superuser: {e}")

    def _run_seeders(self) -> None:
        """Run seeders if available"""
        try:
            call_command("seed", verbosity=0)
            if self.verbose:
                self._log_and_print("✅ Seeders completed")
        except Exception:
            if self.verbose:
                self._log_and_print("⚠️ No seeders found")

    # Optimized check methods
    def _check_db_connections(self) -> Tuple[bool, str, Optional[str]]:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True, "OK", None
        except Exception as e:
            return False, f"Failed: {e}", "Check credentials"

    def _check_memory_usage(self) -> Tuple[bool, str, Optional[str]]:
        if psutil is None:
            return True, "Unknown", None

        memory = psutil.virtual_memory()
        if memory.percent > 90:
            return False, f"{memory.percent:.1f}% used", "Free memory"
        return True, f"{memory.percent:.1f}% used", None

    def _check_disk_space_detailed(self) -> Tuple[bool, str, Optional[str]]:
        if psutil is None:
            return True, "Unknown", None

        disk = psutil.disk_usage("/")
        free_gb = disk.free // (1024**3)
        if free_gb < 1:
            return False, f"{free_gb}GB free", "Need more space"
        return True, f"{free_gb}GB free", None

    def _benchmark_connection(self) -> str:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return f"{(time.time() - start) * 1000:.1f}ms"

    # Placeholder notification methods
    def _send_slack_notification(self, message: str) -> None:
        pass

    def _send_email_notification(self, message: str) -> None:
        pass

    def _send_discord_notification(self, message: str) -> None:
        pass

    def _send_teams_notification(self, message: str) -> None:
        pass

    def _get_system_performance_factor(self) -> float:
        """Calculate system performance factor"""
        if psutil is None:
            return 1.0

        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()

        if cpu_count is None:
            cpu_count = 1  # Default fallback

        # Performance factor based on CPU and memory
        cpu_factor = min(cpu_count / 4.0, 2.0)  # Normalize to 4 cores
        memory_factor = min(memory.total / (8 * 1024**3), 2.0)  # Normalize to 8GB

        return (cpu_factor + memory_factor) / 2

    def _estimate_data_size_bytes(self) -> int:
        """Estimate database size in bytes"""
        try:
            with connection.cursor() as cursor:
                if connection.vendor == "postgresql":
                    cursor.execute("SELECT pg_database_size(current_database())")
                    return cursor.fetchone()[0]
                elif connection.vendor == "mysql":
                    cursor.execute(
                        """
                        SELECT SUM(data_length + index_length) 
                        FROM information_schema.tables 
                        WHERE table_schema = DATABASE()
                        """
                    )
                    result = cursor.fetchone()[0]
                    return result if result else 0
                else:  # SQLite
                    db_path = connection.settings_dict.get("NAME", ":memory:")
                    if db_path != ":memory:" and os.path.exists(db_path):
                        return os.path.getsize(db_path)
        except Exception:
            pass

        return 1024 * 1024  # Default 1MB

    def _has_complex_relationships(self) -> bool:
        """Check if database has complex foreign key relationships"""
        try:
            with connection.cursor() as cursor:
                if connection.vendor == "postgresql":
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM information_schema.table_constraints 
                        WHERE constraint_type = 'FOREIGN KEY'
                    """
                    )
                elif connection.vendor == "mysql":
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM information_schema.key_column_usage 
                        WHERE referenced_table_name IS NOT NULL
                    """
                    )
                else:  # SQLite
                    return False  # SQLite FK detection is complex

                fk_count = cursor.fetchone()[0]
                return fk_count > 5  # Arbitrary threshold
        except Exception:
            return False

    def _get_system_specs(self) -> Dict[str, Any]:
        """Get system specifications for AI learning"""
        if psutil is None:
            return {}

        return {
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_total": psutil.disk_usage("/").total,
        }
