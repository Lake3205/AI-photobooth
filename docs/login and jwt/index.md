# Authentication and JWT

This document provides an overview of the authentication system in our application. It covers the login process, JWT token generation and verification, and how routes are protected using role-based access control.

## Overview

Our authentication system uses JSON Web Tokens (JWT) to secure API endpoints. Users log in with their credentials, receive a JWT token, and include this token in subsequent requests to access protected routes. The system supports role-based access control, allowing different levels of access for different user types.

## Setup

To set up the authentication system, ensure the following configurations are in place:

1. **JWT Secret Key**: Add a secret key to your `.env` file in the backend directory:
   ```
   JWT_SECRET_KEY= #TODO een key maken
   ```
   This key is used to sign and verify JWT tokens.

2. **Database Configuration**: Ensure the users table exists in your MariaDB database. Users should have the following fields:
   - `id`: Unique identifier
   - `username`: User's login name
   - `hashed_password`: Bcrypt-hashed password
   - `role`: User role (e.g., "admin")

3. **Install Dependencies**: The authentication system requires the following Python packages:
   ```
   pip install -r requirements.txt
   ```
   Key dependencies include:
   - `python-jose[cryptography]` for JWT handling
   - `passlib[bcrypt]` for password hashing
   - `python-multipart` for form data parsing

## Login Process

The login process follows these steps:

### Backend Flow

1. **Credential Submission**: The client sends a POST request to `/api/auth/login` with username and password:
   ```json
   {
     "username": "user123",
     "password": "password123"
   }
   ```

2. **User Verification**: The system queries the database for the user by username using `get_user_by_username()` in `backend/services/database_service.py`.

3. **Password Validation**: The plain-text password is verified against the hashed password using bcrypt through `verify_password()` in `backend/services/auth_service.py`.

4. **Token Generation**: If credentials are valid, a JWT token is created using `create_access_token()` with the following payload:
   - `sub`: Username
   - `role`: User role
   - `exp`: Expiration timestamp (8 hours by default)

5. **Token Response**: The server returns the token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

### Frontend Flow

The frontend authentication service (`frontend/src/services/authService.ts`) handles the login process:

1. **Login Request**: Sends credentials to the backend login endpoint.

2. **Token Storage**: Stores the received JWT token in localStorage under the key `user_token`.

3. **Token Verification**: Immediately verifies the token by calling `/api/auth/verify` to ensure it's valid.

4. **User Information**: Stores the username in localStorage for display purposes.

## Token Configuration

JWT tokens are configured in `backend/constants/auth.py`:

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration Time**: 480 minutes (8 hours)
- **Token Payload**: Contains username (`sub`) and user role

## Route Protection

Routes are protected using FastAPI dependency injection. The system provides two levels of protection:

### Basic Authentication

Any route that requires an authenticated user uses the `get_current_user` dependency:

```python
from controllers.auth_controller import get_current_user

@router.get("/protected-route")
async def protected_route(user = Depends(get_current_user)):
    return {"message": f"Hello, {user['username']}"}
```

The `get_current_user` dependency:
1. Extracts the Bearer token from the `Authorization` header
2. Verifies the token using `verify_token()` from `auth_service.py`
3. Decodes the JWT to extract the username
4. Fetches the user from the database
5. Returns the user object or raises a 401 Unauthorized error

### Admin Role Protection

Routes that require admin access use the `require_admin` dependency:

```python
from controllers.auth_controller import require_admin

@router.get("/admin-only")
async def admin_route(user = Depends(require_admin)):
    return {"message": "Admin access granted"}
```

The `require_admin` dependency:
1. First calls `get_current_user` to authenticate the user
2. Checks if the user's role is "admin"
3. Returns the user object if admin, or raises a 403 Forbidden error

### Current Protected Routes

The following routes in the application are currently protected:

- **`GET /api/auth/verify`**: Requires authentication (uses `get_current_user`)
  - Verifies the current user's token is valid
  - Returns user information: username, role, and authentication status

- **`GET /database/assumptions/{ai_model}`**: Requires admin role (uses `require_admin`)
  - Retrieves all stored assumptions for a specific AI model
  - Only accessible by users with admin role

## Frontend Token Management

The frontend `authService` provides utilities for managing authentication:

### Authentication Methods

- **`login(credentials)`**: Authenticates user and stores token
- **`logout()`**: Removes token and username from localStorage
- **`getToken()`**: Retrieves the stored JWT token
- **`isAuthenticated()`**: Checks if a token exists
- **`verifyToken()`**: Validates the current token with the backend

### Authenticated Requests

For making authenticated API calls, use the `authenticatedFetch()` method:

```typescript
const response = await authService.authenticatedFetch(
  'http://localhost:8000/database/assumptions/claude',
  { method: 'GET' }
)
```

This method:
1. Automatically adds the `Authorization: Bearer <token>` header
2. Handles 401 errors by logging out and redirecting to login
3. Handles 403 errors by redirecting to the selfie page
4. Returns the response for successful requests

## Security Considerations

### Password Security

- Passwords are hashed using **bcrypt** with automatic salt generation
- Plain-text passwords are never stored in the database
- The `passlib` library handles the hashing with secure defaults

### Token Security

- Tokens expire after 8 hours to limit the window of vulnerability
- The secret key should be kept secure and never committed to version control
- Tokens are signed to prevent tampering
- Token validation occurs on every protected request

### Error Handling

The system provides appropriate error responses:
- **401 Unauthorized**: Invalid credentials or expired token
- **403 Forbidden**: Valid token but insufficient permissions (not admin)
- Detailed error messages help with debugging without exposing sensitive information

## Verification Endpoint

The `/api/auth/verify` endpoint serves multiple purposes:

1. **Token Validation**: Confirms the token is valid and not expired
2. **User Information**: Returns current user's username and role
3. **Frontend State**: Used by the frontend to maintain authentication state across page reloads

Example response:
```json
{
  "username": "admin_user",
  "role": "admin",
  "authenticated": true
}
```

## Implementation Files

The authentication system is implemented across several files:

- **`backend/controllers/auth_controller.py`**: Defines login endpoint and protection dependencies
- **`backend/services/auth_service.py`**: Handles password hashing, token creation, and verification
- **`backend/services/database_service.py`**: Provides `get_user_by_username()` for user lookup
- **`backend/constants/auth.py`**: Configuration constants (secret key, algorithm, expiration)
- **`backend/models/user.py`**: Pydantic models for User, UserLogin, Token, and TokenData
- **`frontend/src/services/authService.ts`**: Frontend authentication service for login and token management

## Creating User / Adding User

To add a new user to the system, use the `generate_user_db.py` script located in the `backend/` directory. This script generates a bcrypt-hashed password and provides an SQL INSERT statement to add the user to the database.

### Using the Script

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the user generator script:
   ```bash
   python generate_user_db.py
   ```

3. Follow the prompts:
   - **Enter the password**: Type the desired password for the new user
   - **Enter the username**: Type the username (defaults to "user" if left empty)

4. The script will output:
   - The generated bcrypt hash
   - An SQL INSERT statement ready to execute

### Example Usage

```
=== User Generator ===

Enter the password: mySecurePassword123

=== Generated Hash ===
$2b$12$KIXl2eF8H9p3Qw5vN6mZxOz.7dQYr8sT3uV4wX5yZ6aB7cD8eF9gH

Enter the username (default: user): admin_user

=== SQL Insert Statement ===
SQL script for DB:

INSERT INTO users (username, hashed_password, role) VALUES ('admin_user', '$2b$12$KIXl2eF8H9p3Qw5vN6mZxOz.7dQYr8sT3uV4wX5yZ6aB7cD8eF9gH', 'user');

=== Done ===
```

### Adding the User to the Database

1. Copy the generated SQL INSERT statement
2. Connect to phpmyadmin (VPS)
3. Execute the SQL statement to create the user
4. If you want to make the user an admin, change `'user'` to `'admin'` in the role field before executing:
   ```sql
   INSERT INTO users (username, hashed_password, role) 
   VALUES ('admin_user', '$2b$12$...', 'admin');
   ```

### Notes

- The script uses bcrypt with automatic salt generation for secure password hashing
- Each time you run the script with the same password, it will generate a different hash (due to the salt)
- The default role is `'user'` - modify it to `'admin'` if the user needs admin privileges
- Make sure your `users` table exists in the database before inserting users

