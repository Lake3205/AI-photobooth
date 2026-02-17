#!/usr/bin/env python3
"""
Migration File Generator
Creates a new migration file with the correct naming convention and template
"""
import sys
from datetime import datetime
from pathlib import Path


def create_migration(description: str):
    """Create a new migration file"""
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Clean description for filename
    clean_desc = description.lower().replace(' ', '_').replace('-', '_')
    clean_desc = ''.join(c for c in clean_desc if c.isalnum() or c == '_')
    
    # Create filename
    filename = f"{timestamp}_{clean_desc}.sql"
    
    # Migration template
    template = f"""-- Migration: {description}
-- Created: {datetime.now().strftime('%Y-%m-%d')}
-- Description: Add detailed description of what this migration does

-- UP
-- Add your schema changes here
-- Example:
-- CREATE TABLE example (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL
-- );

-- DOWN
-- Add rollback statements here
-- Example:
-- DROP TABLE IF EXISTS example;
"""
    
    # Get migrations directory
    db_dir = Path(__file__).parent
    migrations_dir = db_dir / "migrations" / "versions"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    # Create file
    filepath = migrations_dir / filename
    
    if filepath.exists():
        print(f"✗ Migration file already exists: {filename}")
        return False
    
    filepath.write_text(template, encoding='utf-8')
    
    print(f"✓ Created migration: {filename}")
    print(f"  Location: {filepath}")
    print(f"\nNext steps:")
    print(f"  1. Edit the file and add your SQL changes")
    print(f"  2. Test with: python migrate.py up")
    print(f"  3. Verify with: python migrate.py status")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python new_migration.py <description>")
        print("\nExamples:")
        print("  python new_migration.py 'add user avatars'")
        print("  python new_migration.py 'create sessions table'")
        print("  python new_migration.py 'add indexes for performance'")
        sys.exit(1)
    
    description = ' '.join(sys.argv[1:])
    
    if not description.strip():
        print("✗ Description cannot be empty")
        sys.exit(1)
    
    try:
        create_migration(description)
    except Exception as e:
        print(f"✗ Error creating migration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
