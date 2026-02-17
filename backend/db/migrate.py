#!/usr/bin/env python3
"""
Database Migration Manager
Handles running migrations, rollbacks, and tracking schema versions
"""
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import mariadb
    from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
except ImportError as e:
    print(f"✗ Error importing dependencies: {e}")
    print("Make sure you have mariadb installed: pip install mariadb")
    sys.exit(1)


class MigrationManager:
    """Manages database migrations"""
    
    def __init__(self):
        self.db_dir = Path(__file__).parent
        self.migrations_dir = self.db_dir / "migrations" / "versions"
        self.connection = None
        self.cursor = None
        
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mariadb.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                autocommit=False
            )
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to database: {DB_NAME}@{DB_HOST}:{DB_PORT}")
            return True
        except mariadb.Error as e:
            print(f"✗ Error connecting to database: {e}")
            print(f"  Host: {DB_HOST}:{DB_PORT}")
            print(f"  Database: {DB_NAME}")
            print(f"  User: {DB_USER}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
    def ensure_migrations_table(self):
        """Create schema_migrations table if it doesn't exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_version (version)
                )
            """)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"✗ Error creating migrations table: {e}")
            self.connection.rollback()
            raise
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions"""
        try:
            self.cursor.execute(
                "SELECT version FROM schema_migrations ORDER BY applied_at"
            )
            return [row[0] for row in self.cursor.fetchall()]
        except mariadb.Error:
            return []
    
    def get_available_migrations(self) -> List[Tuple[str, Path]]:
        """Get list of available migration files"""
        if not self.migrations_dir.exists():
            return []
        
        migrations = []
        pattern = re.compile(r'^\d{8}_\d{6}_.*\.sql$')
        
        for file in sorted(self.migrations_dir.glob("*.sql")):
            if pattern.match(file.name):
                version = file.stem
                migrations.append((version, file))
        
        return migrations
    
    def parse_migration(self, filepath: Path) -> Tuple[str, str]:
        """Parse migration file into UP and DOWN sections"""
        content = filepath.read_text(encoding='utf-8')
        
        # Find UP and DOWN markers
        up_match = re.search(r'--\s*UP\s*\n', content, re.IGNORECASE)
        down_match = re.search(r'--\s*DOWN\s*\n', content, re.IGNORECASE)
        
        if not up_match or not down_match:
            raise ValueError(
                f"Migration {filepath.name} must contain '-- UP' and '-- DOWN' sections"
            )
        
        up_start = up_match.end()
        down_start = down_match.end()
        
        # Extract sections
        up_sql = content[up_start:content.index('-- DOWN', up_start)].strip()
        down_sql = content[down_start:].strip()
        
        return up_sql, down_sql
    
    def execute_sql(self, sql: str):
        """Execute SQL statements, handling multiple statements"""
        # Split by semicolon but respect strings and comments
        statements = []
        current = []
        in_string = False
        in_comment = False
        
        for line in sql.split('\n'):
            line = line.strip()
            
            # Skip empty lines and comment-only lines
            if not line or line.startswith('--'):
                continue
            
            current.append(line)
            
            # Check if statement is complete (ends with semicolon)
            if line.endswith(';'):
                statement = ' '.join(current)
                if statement and not statement.startswith('--'):
                    statements.append(statement)
                current = []
        
        # Execute each statement
        for statement in statements:
            if statement.strip():
                try:
                    self.cursor.execute(statement)
                except mariadb.Error as e:
                    print(f"✗ Error executing SQL: {e}")
                    print(f"  Statement: {statement[:100]}...")
                    raise
    
    def apply_migration(self, version: str, filepath: Path):
        """Apply a single migration"""
        print(f"  Applying: {version}")
        
        try:
            up_sql, _ = self.parse_migration(filepath)
            
            # Execute migration
            self.execute_sql(up_sql)
            
            # Record migration
            self.cursor.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (version,)
            )
            
            self.connection.commit()
            print(f"    ✓ Applied: {version}")
            
        except Exception as e:
            print(f"    ✗ Failed: {version}")
            print(f"       Error: {e}")
            self.connection.rollback()
            raise
    
    def rollback_migration(self, version: str, filepath: Path):
        """Rollback a single migration"""
        print(f"  Rolling back: {version}")
        
        try:
            _, down_sql = self.parse_migration(filepath)
            
            # Execute rollback
            self.execute_sql(down_sql)
            
            # Remove migration record
            self.cursor.execute(
                "DELETE FROM schema_migrations WHERE version = ?",
                (version,)
            )
            
            self.connection.commit()
            print(f"    ✓ Rolled back: {version}")
            
        except Exception as e:
            print(f"    ✗ Failed: {version}")
            print(f"       Error: {e}")
            self.connection.rollback()
            raise
    
    def migrate_up(self):
        """Run all pending migrations"""
        self.ensure_migrations_table()
        
        applied = set(self.get_applied_migrations())
        available = self.get_available_migrations()
        
        pending = [(v, p) for v, p in available if v not in applied]
        
        if not pending:
            print("✓ No pending migrations")
            return
        
        print(f"\nFound {len(pending)} pending migration(s):\n")
        
        for version, filepath in pending:
            self.apply_migration(version, filepath)
        
        print(f"\n✓ Successfully applied {len(pending)} migration(s)\n")
    
    def migrate_down(self, count: int = 1):
        """Rollback the last N applied migrations"""
        applied = self.get_applied_migrations()
        
        if not applied:
            print("✓ No migrations to rollback")
            return
        
        available = dict(self.get_available_migrations())
        to_rollback = applied[-count:]
        
        if len(to_rollback) < count:
            print(f"⚠️  Only {len(to_rollback)} migration(s) available to rollback")
        
        print(f"\nRolling back {len(to_rollback)} migration(s):\n")
        
        for version in reversed(to_rollback):
            if version not in available:
                print(f"✗ Migration file not found: {version}")
                continue
            
            self.rollback_migration(version, available[version])
        
        print(f"\n✓ Successfully rolled back {len(to_rollback)} migration(s)\n")
    
    def status(self):
        """Show migration status"""
        self.ensure_migrations_table()
        
        applied = set(self.get_applied_migrations())
        available = self.get_available_migrations()
        
        print("\n" + "="*70)
        print("DATABASE MIGRATION STATUS")
        print("="*70)
        print(f"Database: {DB_NAME}@{DB_HOST}:{DB_PORT}")
        print("="*70 + "\n")
        
        if not available:
            print("No migration files found")
            print("\nCreate migrations in: backend/db/migrations/versions/")
            print("="*70 + "\n")
            return
        
        for version, filepath in available:
            status = "✓ APPLIED " if version in applied else "  PENDING "
            print(f"{status} {version}")
        
        print("\n" + "="*70)
        print(f"Applied: {len(applied)} / {len(available)} migrations")
        print("="*70 + "\n")
    
    def reset(self):
        """Reset database by rolling back all migrations"""
        print("\n" + "="*70)
        print("⚠️  WARNING: DATABASE RESET")
        print("="*70)
        print("This will drop all tables and remove all data!")
        print("="*70 + "\n")
        
        response = input("Type 'RESET' to confirm: ")
        
        if response != 'RESET':
            print("✓ Reset cancelled\n")
            return
        
        applied = self.get_applied_migrations()
        available = dict(self.get_available_migrations())
        
        if not applied:
            print("✓ No migrations to rollback\n")
            return
        
        print(f"\nRolling back {len(applied)} migration(s):\n")
        
        for version in reversed(applied):
            if version in available:
                self.rollback_migration(version, available[version])
        
        print("\n✓ Database reset completed\n")


def print_usage():
    """Print usage information"""
    print("""
Database Migration Manager

Usage: python migrate.py [command] [options]

Commands:
  status              Show migration status
  up                  Run all pending migrations
  down [count]        Rollback last migration (or N migrations)
  reset               Reset database (rollback all migrations)

Examples:
  python migrate.py status         # Check migration status
  python migrate.py up             # Run all pending migrations
  python migrate.py down           # Rollback last migration
  python migrate.py down 3         # Rollback last 3 migrations
  python migrate.py reset          # Reset entire database

Environment:
  Configure database connection in .env.development:
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=darktech_user
    DB_PASSWORD=password
    DB_NAME=darktech
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command not in ['status', 'up', 'down', 'reset']:
        print(f"✗ Unknown command: {command}\n")
        print_usage()
        sys.exit(1)
    
    manager = MigrationManager()
    
    try:
        if not manager.connect():
            sys.exit(1)
        
        if command == "status":
            manager.status()
        elif command == "up":
            manager.migrate_up()
        elif command == "down":
            count = 1
            if len(sys.argv) > 2:
                try:
                    count = int(sys.argv[2])
                except ValueError:
                    print(f"✗ Invalid count: {sys.argv[2]}")
                    sys.exit(1)
            manager.migrate_down(count)
        elif command == "reset":
            manager.reset()
            
    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        sys.exit(1)
    finally:
        manager.close()


if __name__ == "__main__":
    main()
