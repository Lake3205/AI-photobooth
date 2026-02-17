# Local Database Setup - Quick Start Guide

This guide will help you set up and run a local MariaDB database for development.

## Prerequisites

- Docker Desktop installed and running
- Python 3.8+ with mariadb package installed

## Step 1: Create Environment File

Create or update `.env.development` in the project root:

```bash
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Local Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=darktech_user
DB_PASSWORD=password
DB_NAME=darktech

# JWT Configuration
JWT_SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256

SHOW_REASONING=true

# Frontend API URL
VITE_API_URL=http://localhost:8000
```

## Step 2: Start Local Database

From the project root directory:

```bash
# Start just the database
docker-compose up -d db

# Or start database with phpMyAdmin (recommended)
docker-compose up -d db phpmyadmin
```

Wait for the database to be healthy (about 10-15 seconds).

## Step 3: Run Migrations

```bash
cd backend/db
python migrate.py up
```

You should see:
```
✓ Connected to database: darktech@localhost:3306
Found 1 pending migration(s):
  Applying: 20260217_120000_initial_schema
    ✓ Applied: 20260217_120000_initial_schema
✓ Successfully applied 1 migration(s)
```

## Step 4: Verify Setup

Check migration status:
```bash
python migrate.py status
```

Access phpMyAdmin:
- URL: http://localhost:8080
- Username: `darktech_user`
- Password: `password`

## Useful Commands

### Database Management

```bash
# Check if database is running
docker ps | grep ai-photobooth-db

# View database logs
docker logs ai-photobooth-db

# Stop database
docker-compose stop db

# Restart database
docker-compose restart db

# Remove database and all data
docker-compose down -v
```

### Migration Commands

```bash
cd backend/db

# Check status
python migrate.py status

# Run migrations
python migrate.py up

# Rollback last migration
python migrate.py down

# Rollback multiple migrations
python migrate.py down 3

# Reset database (careful!)
python migrate.py reset
```

## Troubleshooting

### Connection Refused

**Problem:** Can't connect to database

**Solution:**
1. Check if Docker is running: `docker ps`
2. Check if db container is healthy: `docker ps | grep ai-photobooth-db`
3. Wait a few seconds after starting the database
4. Verify port 3306 is not used by another service

### Migration Errors

**Problem:** Migration fails with SQL error

**Solution:**
1. Check migration syntax in the .sql file
2. Verify database is accessible: `docker exec -it ai-photobooth-db mariadb -u darktech_user -p darktech`
3. Check migration status: `python migrate.py status`
4. If needed, reset and try again: `python migrate.py reset` then `python migrate.py up`

### Python Import Errors

**Problem:** Module not found errors

**Solution:**
```bash
# Activate your virtual environment
cd backend
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # Linux/Mac

# Install/update dependencies
pip install mariadb python-dotenv
```

## Development Workflow

1. **Start your development session:**
   ```bash
   docker-compose up -d db phpmyadmin
   cd backend/db
   python migrate.py status
   ```

2. **Make a schema change:**
   - Create new migration file in `backend/db/migrations/versions/`
   - Name it: `YYYYMMDD_HHMMSS_description.sql`
   - Add UP and DOWN sections

3. **Apply the migration:**
   ```bash
   python migrate.py up
   ```

4. **End your session:**
   ```bash
   docker-compose stop db phpmyadmin
   ```

## Next Steps

- Add seed data scripts (you'll provide these later)
- Create additional migrations as your schema evolves
- Consider adding a users table seeder with default admin user
