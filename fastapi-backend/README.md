# Notes App Backend

---

## Overview

This project is a **production-ready RESTful backend** built using **FastAPI**.
It provides a secure and scalable system for managing personal notes with authentication, authorization, and clean architecture.

The application demonstrates real-world backend practices including:

* JWT authentication
* Role-based access control
* Database integration with PostgreSQL
* Docker containerization
* API documentation
* Unit testing

---

## Key Features

### Authentication & Authorization

* User registration and login
* JWT-based authentication
* Role-based access control (RBAC)

### Notes Management

* Create, read, update, delete notes (CRUD)
* Users can only access their own notes

### Dockerized Setup

* Fully containerized using Docker & Docker Compose
* Consistent environment across systems

### API Documentation

* Swagger UI → `/docs`
* ReDoc → `/redoc`

### Testing

* Pytest-based test suite
* Covers authentication & notes APIs

### Google OAuth (Optional)

* Login via Google account using Authlib

---

## Project Goal

To build a **clean, scalable, production-like backend system** using best practices:

* Separation of concerns
* Secure authentication
* Modular architecture
* Containerized deployment

---

## Tech Stack

| Category         | Technology        |
| ---------------- | ----------------- |
| Framework        | FastAPI           |
| Database         | PostgreSQL        |
| ORM              | SQLAlchemy        |
| Auth             | JWT (python-jose) |
| Hashing          | Passlib (bcrypt)  |
| Containerization | Docker            |
| Testing          | Pytest            |
| API Client       | Postman           |

---

## Architecture Overview

```
Client → API Routes → Dependencies → Services → Database → Response
```

---

## Project Structure

```
app/
├── main.py
│
├── core/
│   ├── config.py
│   ├── security.py
│
├── db/
│   ├── session.py
│   ├── base.py
│
├── models/
│   ├── user.py
│   ├── note.py
│
├── schemas/
│   ├── user.py
│   ├── note.py
│   ├── token.py
│
├── api/
│   ├── deps.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── note.py
│
├── services/
│   ├── user_service.py
│   ├── note_service.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_notes.py
│
.env
requirements.txt
Dockerfile
docker-compose.yml
README.md
```

---

## Local Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

---

### 4. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## Docker Setup

### Build & Run

```bash
docker compose up --build
```

### Run in background

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

---

## Run Tests

```bash
pytest
```

---

## API Endpoints

### Auth

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| POST   | `/auth/register` | Register user    |
| POST   | `/auth/login`    | Login user       |
| GET    | `/auth/me`       | Get current user |

---

### Notes

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| POST   | `/notes`      | Create note   |
| GET    | `/notes`      | Get all notes |
| GET    | `/notes/{id}` | Get note      |
| PUT    | `/notes/{id}` | Update note   |
| DELETE | `/notes/{id}` | Delete note   |

---

## FastAPI Service

This service is responsible for handling authentication and note-related functionality for the Team Productivity Platform.

### Responsibilities

* Authentication
* User Management
* Notes Management
* Open Library Integration
* Note-to-Task Conversion

### Base URL

```http
http://localhost:8000/api/v1
```

### Health Check

```http
GET /health
```

Example Response:

```json
{
  "status": "healthy"
}
```

### Service Ownership

The FastAPI service owns:

#### Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

#### Notes

```http
POST   /notes
GET    /notes
GET    /notes/{id}
PUT    /notes/{id}
DELETE /notes/{id}
```

#### Future Endpoints

```http
GET  /users/me
PUT  /users/me

GET  /books/search

POST /notes/{id}/convert-to-tasks
```

### Integration

This service will be consumed by:

* Next.js Frontend
* NestJS Productivity Service

Authentication is shared across services using JWT tokens.

Users authenticate once and can access resources managed by both FastAPI and NestJS without logging in again.

---

## Authentication

FastAPI acts as the authentication provider for the entire platform.

Users authenticate once and receive a JWT access token.

The same JWT token is later validated by both:

* FastAPI
* NestJS

This creates a Single Login Experience across services.

**JWT Claims**

Example:
```text
{
  "sub": "1",
  "email": "user@example.com",
  "role": "ADMIN"
}
```

**Claims include:**
```text
User ID
Email
Role
Role-Based Access Control (RBAC)
```

The platform currently supports:

**ADMIN**

*Capabilities:*
- View all users
- View all notes
- Manage all notes
- View system analytics
- View activity logs
- Access administrative dashboards


**MEMBER**

*Capabilities:*
- Manage own notes
- View own information
- Access personal productivity data

**Notes Module**

The Notes module serves as the knowledge-management component of the platform.

**Features:**

- Create Notes
- View Notes
- Update Notes
- Delete Notes
- Pagination
- Search Ready
- Sorting Ready


**Notes API**
Create Note

```text
POST /api/v1/notes
```

Creates a note owned by the authenticated user.

**Get Notes**
```text
GET /api/v1/notes
```

*Supports:*

- Pagination
- Search (planned)
- Sorting (planned)

Example:

```text
GET /api/v1/notes?page=1&limit=10
```

*Get Note By ID*
```text
GET /api/v1/notes/{note_id}
```

**Access Rules:**

- MEMBER → Own notes only
- ADMIN → Any note

*Update Note*

```text
PUT /api/v1/notes/{note_id}
```

**Access Rules:**

- MEMBER → Own notes only
- ADMIN → Any note

*Delete Note*
```text
DELETE /api/v1/notes/{note_id}
```

**Access Rules:**

MEMBER → Own notes only
ADMIN → Any note

---

### Benefits

* Improves performance
* Reduces server load
* Better user experience for large datasets

* Note: Pagination can be easily re-enabled in the API by adding `page` and `limit` query parameters in the `/notes` route.

---

## Shared JWT Contract

JWT must work across FastAPI and NestJS.

**Required payload:**
```text
{
  "sub": "1",
  "email": "user@example.com",
  "role": "ADMIN",
  "iss": "team-productivity-platform",
  "aud": "team-productivity-users",
  "type": "access"
}
```

NestJS must be able to authorize users without additional database lookups.

---

## Database Layer

The FastAPI service uses SQLAlchemy 2.x with PostgreSQL as the primary database.

### Responsibilities

The database layer is responsible for:

* Managing PostgreSQL connections
* Creating and managing SQLAlchemy sessions
* Providing database dependencies to FastAPI routes and services
* Supporting production-grade connection pooling
* Enabling transaction-safe request handling

### Database Configuration

The application uses a centralized database configuration through environment variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=team_productivity
DB_USER=postgres
DB_PASSWORD=password
```

The SQLAlchemy engine is configured with:

* Connection pooling
* Automatic connection health checks (`pool_pre_ping`)
* Connection recycling
* Debug SQL logging in development environments

### Session Management

A dedicated `SessionLocal` factory creates database sessions for each request.

FastAPI's dependency injection system ensures:

* One session per request
* Automatic cleanup after request completion
* Safe transaction handling

### Service Ownership

FastAPI currently owns the following database modules:

* Users
* Authentication
* Notes
* Open Library Integrations

NestJS may connect to the same PostgreSQL database using its own ORM (TypeORM or Prisma) while maintaining clear service boundaries.

### Architecture

```text
Next.js Frontend
        │
        ▼
     FastAPI
        │
        ▼
   SQLAlchemy ORM
        │
        ▼
    PostgreSQL

NestJS
   │
   └── Can access the same PostgreSQL instance
       through its own ORM layer
```

This architecture supports the Team Productivity Platform's multi-service design while maintaining a shared and scalable database infrastructure.

---

## User Model

The User model is the central identity and authorization entity within the FastAPI service.

FastAPI acts as the authentication authority and is responsible for issuing JWT tokens that are consumed by both FastAPI and NestJS services.

### Responsibilities

* User Registration
* User Authentication
* Role-Based Access Control (RBAC)
* JWT Identity Source
* User Ownership Validation

### User Fields

| Field           | Type     | Description                 |
| --------------- | -------- | --------------------------- |
| id              | Integer  | Primary Key                 |
| email           | String   | Unique user email           |
| hashed_password | String   | Securely hashed password    |
| role            | String   | User role (ADMIN or MEMBER) |
| is_active       | Boolean  | User account status         |
| created_at      | DateTime | User creation timestamp     |
| updated_at      | DateTime | Last update timestamp       |

### Supported Roles

#### ADMIN

Permissions:

* View all users
* View all notes
* Manage all notes
* Access analytics dashboard
* Access activity logs
* Access administration features

#### MEMBER

Permissions:

* Manage own notes
* View own notes
* Update own notes
* Delete own notes
* View personal analytics

### JWT Integration

FastAPI generates JWT tokens using user information.

Example JWT Payload:

```json
{
  "sub": "1",
  "email": "admin@example.com",
  "role": "ADMIN",
  "iss": "team-productivity-platform",
  "aud": "team-productivity-users",
  "type": "access"
}
```

This JWT is shared across:

* Next.js Frontend
* FastAPI Service
* NestJS Service

This enables a Single Login Experience across the platform.

### Relationships

User → Notes

```text
User
 └── Notes (One-to-Many)
```

A user can own multiple notes.

### Database Optimizations

Indexes are created on:

* email
* role
* is_active

These indexes improve:

* Authentication performance
* Admin dashboard queries
* Analytics reporting
* User management operations

---

## Note Model

The Note model is owned entirely by the FastAPI service.

Notes represent user-created content and serve as the foundation for future task generation workflows.

### Responsibilities

* Note Creation
* Note Updates
* Note Deletion
* Note Search
* Note Filtering
* Open Library Integration
* Note-to-Task Conversion Source

### Note Fields

| Field                | Type     | Description              |
| -------------------- | -------- | ------------------------ |
| id                   | Integer  | Primary Key              |
| title                | String   | Note title               |
| content              | Text     | Note content             |
| owner_id             | Integer  | User ownership reference |
| book_reference_id    | String   | Open Library reference   |
| is_converted_to_task | Boolean  | Task conversion status   |
| created_at           | DateTime | Creation timestamp       |
| updated_at           | DateTime | Last update timestamp    |

### Ownership Rules

#### MEMBER

Can:

* View own notes
* Update own notes
* Delete own notes

#### ADMIN

Can:

* View any note
* Update any note
* Delete any note
* Access all notes endpoint

### Open Library Integration

Notes can contain book references retrieved from the Open Library API.

Example:

```json
{
  "title": "Learning React",
  "book_reference_id": "OL45883W"
}
```

This allows users to associate learning resources directly with notes.

### Note-to-Task Conversion

A note can be converted into one or more tasks.

Workflow:

```text
FastAPI Note
        │
        ▼
Convert To Task
        │
        ▼
NestJS Task Service
        │
        ▼
Task Created
        │
        ▼
is_converted_to_task = true
```

This preserves clear ownership boundaries:

FastAPI owns:

* Notes
* Note Content
* Book References

NestJS owns:

* Tasks
* Task Status
* Notifications
* Analytics
* Activity Logs

### Relationships

User → Notes

```text
User (1)
   │
   ▼
Notes (Many)
```

### Database Optimizations

Indexes are created on:

* owner_id
* title
* created_at

**Benefits:**

* Faster note search
* Faster pagination
* Faster sorting
* Improved analytics queries

---

## User Management & Authentication Schemas

The User module provides the foundation for authentication, authorization, and cross-service identity management within the Team Productivity Platform.

FastAPI acts as the authentication provider and JWT issuer, while NestJS consumes and validates the same JWT for authorization across platform services.

---

## User Registration

Users can create an account using their email address and password.

### Request

```json
{
  "email": "john.doe@example.com",
  "password": "StrongPassword123!"
}
```

Validation:

* Email must be a valid email address
* Password length: 8–128 characters

---

## User Login

Users authenticate using their registered credentials.

### Request

```json
{
  "email": "john.doe@example.com",
  "password": "StrongPassword123!"
}
```

### Response

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

The returned JWT is used for all authenticated requests to both FastAPI and NestJS services.

---

## User Profile Response

Authenticated user information is returned through profile endpoints.

### Example Response

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "role": "MEMBER",
  "is_active": true,
  "created_at": "2026-06-11T10:00:00Z",
  "updated_at": "2026-06-11T10:00:00Z"
}
```

Fields:

| Field      | Description                |
| ---------- | -------------------------- |
| id         | Unique user identifier     |
| email      | User email address         |
| role       | User role                  |
| is_active  | Account status             |
| created_at | Account creation timestamp |
| updated_at | Last update timestamp      |

---

## Role-Based Access Control (RBAC)

The platform supports two user roles.

### ADMIN

Permissions:

* View all users
* View all notes
* Manage all notes
* Manage all tasks
* Access analytics dashboard
* Access activity logs
* Access admin dashboard

### MEMBER

Permissions:

* Manage own notes
* Manage own tasks
* View personal analytics

---

## Shared JWT Contract

FastAPI is the single JWT issuer for the entire platform.

NestJS validates the same token to provide a seamless authentication experience.

### JWT Payload

```json
{
  "sub": "1",
  "email": "user@example.com",
  "role": "ADMIN",
  "iss": "team-productivity-platform",
  "aud": "team-productivity-users",
  "type": "access"
}
```

### JWT Claims

| Claim | Description       |
| ----- | ----------------- |
| sub   | User ID           |
| email | User email        |
| role  | User role         |
| iss   | Token issuer      |
| aud   | Intended audience |
| type  | Token type        |

---

## Authentication Flow

```text
User
  │
  ▼
FastAPI Login Endpoint
  │
  ▼
JWT Issued
  │
  ▼
Next.js Frontend
  │
  ├──────────────► FastAPI APIs
  │
  └──────────────► NestJS APIs
                        │
                        ▼
                JWT Validation
```

This architecture provides a single login experience across all backend services.

---

## Frontend Integration

The Next.js frontend stores the JWT after login and attaches it to every authenticated request.

Example Authorization Header:

```http
Authorization: Bearer <jwt-token>
```

The same token is accepted by:

* FastAPI
* NestJS

No secondary login flow is required.

---

## M2 Architecture Benefits

This authentication architecture enables:

* Common authentication across services
* Role-based authorization
* Admin and Member dashboards
* Secure API access
* NestJS integration without duplicate authentication
* Future microservice expansion
* Strong TypeScript type generation from OpenAPI schemas

---

## User Service Layer

The User Service Layer contains all business logic related to user management and serves as the primary source of user identity information for authentication, authorization, and role-based access control.

Location:

```text
app/services/user_service.py
```

### Responsibilities

The User Service is responsible for:

* User creation
* User retrieval
* Email uniqueness validation
* User activation and deactivation
* Role-based access control (RBAC)
* User listing for administrators
* Providing user information for JWT authentication

---

## Supported Roles

### ADMIN

Administrators can:

* View all users
* Activate users
* Deactivate users
* Access administrative dashboards
* View system analytics
* Access activity logs

### MEMBER

Members can:

* Access their own profile
* Manage their own notes
* Manage their own tasks
* View personal analytics

---

## User Creation

Service Method:

```python
UserService.create_user()
```

Features:

* Password hashing using bcrypt
* Duplicate email validation
* Default role assignment
* Active account creation

Default Role:

```text
MEMBER
```

---

## User Retrieval

### Get User By Email

Used during authentication.

```python
UserService.get_user_by_email()
```

Purpose:

* Login validation
* Registration validation
* JWT authentication

---

### Get User By ID

```python
UserService.get_user_by_id()
```

Purpose:

* User lookup
* Ownership validation
* Profile retrieval

---

### Get Active User By ID

```python
UserService.get_active_user_by_id()
```

Purpose:

* JWT authentication
* Current user retrieval
* Security validation

Validation:

* User exists
* User account is active

---

## User Administration

### Get All Users

```python
UserService.get_all_users()
```

Supports:

* Admin dashboard
* User monitoring
* Analytics reporting

Features:

* Pagination
* Sorting by creation date

---

### Deactivate User

```python
UserService.deactivate_user()
```

Access:

```text
ADMIN only
```

Purpose:

* User moderation
* Account suspension
* Administrative actions

---

### Activate User

```python
UserService.activate_user()
```

Access:

```text
ADMIN only
```

Purpose:

* Restore suspended accounts
* User reactivation

---

## Role-Based Access Control (RBAC)

Centralized RBAC validation is implemented through:

```python
UserService.validate_admin()
```

Validation:

```text
ADMIN → Allowed
MEMBER → Forbidden
```

Used by:

* User administration endpoints
* Analytics endpoints
* Activity log endpoints
* Administrative dashboards

---

## JWT Integration

The User Service provides the identity information used to generate JWT tokens.

JWT Payload:

```json
{
  "sub": "1",
  "email": "user@example.com",
  "role": "ADMIN",
  "iss": "team-productivity-platform",
  "aud": "team-productivity-users",
  "type": "access"
}
```

Fields sourced from:

```python
user.id
user.email
user.role
```

---

## Shared Authentication Architecture

FastAPI acts as the JWT issuer.

NestJS acts as the JWT validator.

The User Service provides the identity information consumed by both services.

```text
User
  ↓
FastAPI Authentication
  ↓
JWT Token
  ↓
Next.js Frontend
  ↓
FastAPI APIs
NestJS APIs
```

This enables a single-login experience across the platform.

---

## Frontend Integration

The Next.js frontend uses user information for:

* Role-based UI rendering
* Profile pages
* Dashboard personalization
* Access control

Examples:

### Admin Dashboard

Visible only to:

```text
ADMIN
```

Features:

* User Management
* Analytics
* Activity Logs

### Member Dashboard

Visible to:

```text
MEMBER
```

Features:

* Notes
* Tasks
* Personal Analytics

---

## M2 Readiness

The User Service is prepared for:

* Shared JWT authentication
* FastAPI ↔ NestJS integration
* Role-based access control
* Admin dashboards
* Analytics reporting
* User management features
* Next.js frontend integration

---

## Testing

This project uses **Pytest** to ensure the correctness of core functionalities.

### Run Tests

```bash
pytest
```

---

### Test Coverage

#### Authentication Tests

* User registration (`/auth/register`)
* User login (`/auth/login`)
* JWT token generation and validation

#### Notes Tests

* Create note (`POST /notes`)
* Get notes (`GET /notes`)
* Authorization using Bearer token
* Ownership validation

---

### Testing Approach

* Uses `TestClient` from FastAPI
* Simulates real API requests
* Tests both success and failure cases
* Ensures authentication is required for protected routes

---

### Example Test Flow

```bash
Register → Login → Get Token → Access Protected Route
```

---

### Why Testing matters?

* Prevents regressions
* Ensures API reliability
* Validates authentication & authorization logic
* Helps maintain production-ready code quality

---

## Final Status

* All tests passing
* Fully functional authentication system
* Secure notes management
* Dockerized backend
* Clean architecture

---


## Postman Collection

This collection helps you test all API endpoints of the Notes Backend easily using Postman.

---

### Import Collection

1. Open **Postman**
2. Click **Import**
3. Select **Raw Text**
4. Paste the JSON below
5. Click **Import**

---

### Base URL

```bash
http://127.0.0.1:8000
```


---

### Collection JSON

```json
{
  "info": {
    "name": "Notes App Backend",
    "_postman_id": "12345-abcde-67890",
    "description": "Postman collection for Notes App",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    },
    {
      "key": "token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/auth/register"
          }
        },
        {
          "name": "Login User",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/auth/login"
          }
        },
        {
          "name": "Get Current User",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/auth/me"
          }
        }
      ]
    },
    {
      "name": "Notes",
      "item": [
        {
          "name": "Create Note",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"title\": \"My Note\",\n  \"content\": \"Hello World\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/notes"
          }
        },
        {
          "name": "Get All Notes",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes"
          }
        },
        {
          "name": "Get Note By ID",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes/1"
          }
        },
        {
          "name": "Update Note",
          "request": {
            "method": "PUT",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"title\": \"Updated Note\",\n  \"content\": \"Updated content\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": "{{base_url}}/notes/1"
          }
        },
        {
          "name": "Delete Note",
          "request": {
            "method": "DELETE",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": "{{base_url}}/notes/1"
          }
        }
      ]
    }
  ]
}
```
---