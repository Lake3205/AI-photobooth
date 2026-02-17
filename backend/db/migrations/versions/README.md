# Migration Files

This directory contains database migration files.

## Naming Convention

Migration files must follow this format:
```
YYYYMMDD_HHMMSS_description.sql
```

Examples:
- `20260217_120000_initial_schema.sql`
- `20260218_140530_add_user_avatars.sql`
- `20260220_093015_add_session_tracking.sql`

## File Structure

Each migration file must contain two sections:

```sql
-- Migration: Brief description
-- Created: YYYY-MM-DD
-- Description: Longer explanation of what this migration does

-- UP
-- SQL statements to apply the migration
CREATE TABLE example (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- DOWN
-- SQL statements to rollback the migration
DROP TABLE IF EXISTS example;
```

## Important Rules

1. **Never modify existing migrations** after they've been applied to any database
2. **Always include both UP and DOWN sections** - migrations must be reversible
3. **Test your DOWN section** - make sure rollback works
4. **Keep migrations atomic** - one logical change per migration
5. **Use IF EXISTS/IF NOT EXISTS** where appropriate for safety

## Example: Adding a Column

```sql
-- Migration: Add profile_picture to users
-- Created: 2026-02-17

-- UP
ALTER TABLE users 
ADD COLUMN profile_picture VARCHAR(512) DEFAULT NULL 
AFTER username;

-- DOWN
ALTER TABLE users 
DROP COLUMN IF EXISTS profile_picture;
```

## Example: Creating a New Table

```sql
-- Migration: Add sessions table for user tracking
-- Created: 2026-02-17

-- UP
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(512) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_sessions_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(token);

-- DOWN
DROP TABLE IF EXISTS sessions;
```

## Generating Timestamps

Use Python to generate timestamp for filenames:

```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
print(f"{timestamp}_your_description.sql")
```

Or in PowerShell:
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Write-Host "${timestamp}_your_description.sql"
```
