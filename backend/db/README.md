# Database Management

This directory contains database schema, migrations, and management scripts for the AI-photobooth project.

## Structure

```
db/
├── migrations/
│   └── versions/          # Migration files
├── create_tables.sql      # Original schema (kept for reference)
├── migrate.py            # Migration manager script
└── README.md             # This file
```

## Local Development Database

### Starting the Local Database

Use Docker Compose to start a local MariaDB instance:

```bash
# Start database (from project root)
docker-compose up -d db

# Start database with phpMyAdmin
docker-compose up -d db phpmyadmin
```

### Configuration

Update your `.env.development` file:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=darktech_user
DB_PASSWORD=password
DB_NAME=darktech
```

### Accessing the Database

**Via phpMyAdmin:**
- URL: http://localhost:8080
- Username: darktech_user (or from .env)
- Password: password (or from .env)

**Via CLI:**
```bash
docker exec -it ai-photobooth-db mariadb -u darktech_user -p darktech
```

## Migration System

### Commands

**Check migration status:**
```bash
cd backend/db
python migrate.py status
```

**Run all pending migrations:**
```bash
python migrate.py up
```

**Rollback last migration:**
```bash
python migrate.py down
```

**Rollback specific number of migrations:**
```bash
python migrate.py down 3
```

**Reset database (drops all tables):**
```bash
python migrate.py reset
```

### Creating a New Migration

1. Create a new file in `migrations/versions/` with format:
   ```
   YYYYMMDD_HHMMSS_description.sql
   ```

2. Structure your migration file:
   ```sql
   -- Migration: Description of changes
   -- Created: YYYY-MM-DD

   -- UP
   CREATE TABLE new_table (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL
   );

   -- DOWN
   DROP TABLE IF EXISTS new_table;
   ```

3. Run the migration:
   ```bash
   python migrate.py up
   ```

### Migration Best Practices

- Always include both UP and DOWN sections
- Test migrations on development database first
- Keep migrations small and focused
- Never modify existing migration files after they've been applied
- Use descriptive names for migrations

## Quick Start

1. **Start local database:**
   ```bash
   docker-compose up -d db
   ```

2. **Run migrations:**
   ```bash
   cd backend/db
   python migrate.py up
   ```

3. **Verify:**
   ```bash
   python migrate.py status
   ```

## Troubleshooting

**Connection refused:**
- Ensure Docker is running
- Check database container: `docker ps | grep db`
- Verify .env.development settings

**Migration fails:**
- Check `python migrate.py status`
- Review error messages
- Verify SQL syntax in migration file

**Reset everything:**
```bash
docker-compose down -v  # Removes database volume
docker-compose up -d db
cd backend/db
python migrate.py up
```
