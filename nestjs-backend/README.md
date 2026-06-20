# Team Productivity Platform - NestJS Backend

## Overview

The NestJS Backend is the second backend service of the Team Productivity Platform.

This service is responsible for task management, categorization, tagging, notifications, analytics, and activity tracking.

The application follows a microservice-inspired architecture where:

- FastAPI owns Authentication and Notes
- NestJS owns Productivity Features
- Next.js acts as the unified frontend
- PostgreSQL is the shared database

NestJS does not perform user authentication.

Authentication is delegated to FastAPI, while NestJS validates the JWT issued by FastAPI to provide a seamless single-login experience.

---

# Responsibilities

## NestJS Service Owns

### Tasks

- Create Tasks
- Update Tasks
- Delete Tasks
- Task Status Management
- Task Priority Management
- Task Querying & Filtering

### Categories

- Create Categories
- Update Categories
- Delete Categories
- Organize Tasks

### Tags

- Create Tags
- Update Tags
- Delete Tags
- Task Tagging

### Notifications

- Notification Listing
- Mark Notifications as Read

### Activity Logs

- Activity History
- User Actions Tracking

### Analytics

- Productivity Dashboard
- Task Statistics
- Completion Metrics

### Public Holiday Integration

- Holiday Awareness
- Due Date Validation
- Sprint Planning Support

---

# Architecture

```text
Next.js Frontend
        │
        ▼

     FastAPI
        │
        ├── Authentication
        ├── User Management
        ├── Notes
        └── Note → Task Conversion

        ▼

      NestJS
        │
        ├── Tasks
        ├── Categories
        ├── Tags
        ├── Notifications
        ├── Analytics
        └── Activity Logs

        ▼

     PostgreSQL
```

---

# Authentication Flow

FastAPI is the JWT issuer.

Flow:

1. User logs in through FastAPI
2. FastAPI generates JWT
3. Frontend stores JWT
4. Frontend sends JWT to FastAPI APIs
5. Frontend sends same JWT to NestJS APIs
6. NestJS validates JWT
7. User accesses all services without re-authentication

---

# Shared JWT Contract

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

NestJS validates:

- JWT Signature
- Issuer
- Audience
- Expiration
- User Role

---

# API Ownership

## FastAPI

### Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Notes

```http
POST   /api/v1/notes
GET    /api/v1/notes
GET    /api/v1/notes/{id}
PUT    /api/v1/notes/{id}
DELETE /api/v1/notes/{id}
```

### Admin

```http
GET /api/v1/notes/admin/all
```

### Conversion

```http
POST /api/v1/notes/{id}/convert-to-task
```

---

## NestJS

### Tasks

```http
POST   /api/v1/tasks
GET    /api/v1/tasks
GET    /api/v1/tasks/:id
PATCH  /api/v1/tasks/:id
DELETE /api/v1/tasks/:id
```

### Categories

```http
POST   /api/v1/categories
GET    /api/v1/categories
GET    /api/v1/categories/:id
PATCH  /api/v1/categories/:id
DELETE /api/v1/categories/:id
```

### Tags

```http
POST   /api/v1/tags
GET    /api/v1/tags
GET    /api/v1/tags/:id
PATCH  /api/v1/tags/:id
DELETE /api/v1/tags/:id
```

### Notifications

```http
GET   /api/v1/notifications
PATCH /api/v1/notifications/:id/read
```

### Analytics

```http
GET /api/v1/analytics/dashboard
```

### Activity Logs

```http
GET /api/v1/activity-logs
```

---

# Database Ownership

## FastAPI Tables

```text
users
notes
```

## NestJS Tables

```text
tasks
categories
tags
task_tags
notifications
activity_logs
```

---

# Technology Stack

## Framework

- NestJS

## Language

- TypeScript

## Database

- PostgreSQL

## ORM

- TypeORM

## Authentication

- Passport JWT
- Shared JWT Validation

## Validation

- class-validator
- class-transformer

## Documentation

- Swagger

## Containerization

- Docker

## Testing

- Jest
- Supertest

---

# Dependencies Installed

## Core NestJS

```bash
npm install @nestjs/config
```

## Database

```bash
npm install @nestjs/typeorm typeorm pg
```

## Authentication

```bash
npm install @nestjs/jwt
npm install passport
npm install passport-jwt
npm install @nestjs/passport
```

Development Types:

```bash
npm install -D @types/passport-jwt
```

## Validation

```bash
npm install class-validator
npm install class-transformer
```

## Swagger

```bash
npm install @nestjs/swagger
npm install swagger-ui-express
```

## Environment Variables

```bash
npm install dotenv
```

## UUID

```bash
npm install uuid
```

## Security

```bash
npm install helmet
```

## Logging

```bash
npm install nestjs-pino
npm install pino
npm install pino-pretty
```

## Testing

```bash
npm install -D supertest
```

## Formatting

```bash
npm install -D prettier
```

## Linting

```bash
npm install -D eslint
npm install -D eslint-config-prettier
npm install -D eslint-plugin-prettier
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/Ashu11122000/Team-Productivity-Platform.git
```

## Navigate to NestJS Backend

```bash
cd Team-Productivity-Platform/nestjs-backend
```

## Install Dependencies

```bash
npm install
```

## Create Environment File

Create:

```text
.env
```

Example:

```env
NODE_ENV=development

PORT=3001

DATABASE_HOST=localhost
DATABASE_PORT=5432

DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

DATABASE_NAME=team_productivity

JWT_SECRET=super-secret-key

JWT_ISSUER=team-productivity-platform
JWT_AUDIENCE=team-productivity-users

FRONTEND_URL=http://localhost:3000
```

---

# Run Development Server

```bash
npm run start:dev
```

Server:

```text
http://localhost:3001
```

---

# Current Development Status

## Completed

### Project Setup

- NestJS Application Created
- TypeScript Configuration
- Dependency Installation
- Folder Structure Design
- Docker Files Added
- Environment Configuration
- Testing Structure Created

### Architecture

- API Ownership Defined
- Authentication Strategy Defined
- Database Ownership Defined
- Shared JWT Contract Defined

### Project Structure

- Configuration Layer
- Database Layer
- Authentication Layer
- Common Utilities Layer
- Feature Modules Layer
- Integrations Layer
- Testing Layer

---

# Next Development Phase

The following modules will now be implemented:

## Configuration

- app.config.ts
- database.config.ts
- jwt.config.ts
- swagger.config.ts

## Database

- TypeORM Configuration
- PostgreSQL Connection

## Bootstrap

- main.ts
- app.module.ts

## Authentication

- JwtStrategy
- JwtAuthGuard
- RolesGuard
- CurrentUser Decorator

## Health Module

```http
GET /health
```

## Tasks Module

First fully implemented business module.

Includes:

- Entity
- DTOs
- CRUD APIs
- Swagger Documentation
- RBAC Support
- Ownership Validation

---

# Architecture

```text
Next.js Frontend
        │
        ▼

     FastAPI
        │
        ├── Authentication
        ├── Users
        ├── Notes
        ├── Open Library
        └── Note → Task Conversion

        ▼

      NestJS
        │
        ├── Tasks
        ├── Categories
        ├── Tags
        ├── Notifications
        ├── Analytics
        └── Activity Logs

        ▼

     PostgreSQL
```

---

# Authentication Strategy

FastAPI is the authentication owner.

NestJS does NOT provide:

* Login APIs
* Registration APIs
* Password Management

Authentication Flow:

1. User logs in via FastAPI.
2. FastAPI generates JWT.
3. Frontend stores JWT.
4. Frontend sends JWT to FastAPI.
5. Frontend sends the same JWT to NestJS.
6. NestJS validates the token.
7. User accesses protected NestJS APIs.

Single Login Experience.

---

# Shared JWT Contract

FastAPI JWT Payload:

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

NestJS will validate:

* JWT Signature
* Issuer
* Audience
* Expiration

---

# Installed Dependencies

Core:

```bash
npm install @nestjs/config
npm install @nestjs/typeorm typeorm pg
npm install @nestjs/jwt @nestjs/passport passport passport-jwt
npm install class-validator class-transformer
npm install @nestjs/swagger swagger-ui-express
npm install helmet
npm install nestjs-pino pino pino-pretty
npm install dotenv
npm install uuid
```

Testing:

```bash
npm install --save-dev supertest
```

TypeORM CLI:

```bash
npm install --save-dev typeorm-ts-node-commonjs
```

---

# Environment Variables

Create a .env file:

```env
NODE_ENV=development

PORT=3001

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=team_productivity

JWT_SECRET=super-secret-key

JWT_ISSUER=team-productivity-platform
JWT_AUDIENCE=team-productivity-users

FRONTEND_URL=http://localhost:3000
```

---

# Phase 1 - Configuration Layer

Files Created:

```text
src/config/app.config.ts
src/config/database.config.ts
src/config/jwt.config.ts
src/config/swagger.config.ts
src/config/index.ts
```

Purpose:

## app.config.ts

Application configuration:

* NODE_ENV
* PORT
* FRONTEND_URL

---

## database.config.ts

Database configuration:

* DATABASE_HOST
* DATABASE_PORT
* DATABASE_USER
* DATABASE_PASSWORD
* DATABASE_NAME

---

## jwt.config.ts

JWT configuration:

* JWT_SECRET
* JWT_ISSUER
* JWT_AUDIENCE

Used later for FastAPI JWT validation.

---

## swagger.config.ts

Swagger setup configuration.

Will expose:

```text
/api/docs
```

Provides:

* OpenAPI Documentation
* JWT Authorization Support
* API Testing Interface

---

## index.ts

Centralized configuration exports.

---

# Phase 2 - Database Layer

Files Created:

```text
src/database/data-source.ts
```

Purpose:

* PostgreSQL Connection
* TypeORM DataSource
* Migration Support
* CLI Integration

Configuration Highlights:

```typescript
synchronize: false
```

Production-safe configuration.

Database changes will be managed using migrations.

---

# Migration Strategy

Future Structure:

```text
src/database/

├── migrations/
│   ├── create-tasks.ts
│   ├── create-categories.ts
│   ├── create-tags.ts
│   ├── create-task-tags.ts
│   ├── create-notifications.ts
│   └── create-activity-logs.ts
│
└── data-source.ts
```

No migrations have been created yet because entities are not implemented.

---

# TypeORM Scripts

package.json:

```json
{
  "scripts": {
    "typeorm": "typeorm-ts-node-commonjs -d src/database/data-source.ts",
    "migration:create": "npm run typeorm -- migration:create src/database/migrations/Migration",
    "migration:generate": "npm run typeorm -- migration:generate src/database/migrations/AutoMigration",
    "migration:run": "npm run typeorm -- migration:run",
    "migration:revert": "npm run typeorm -- migration:revert"
  }
}
```

---

# Phase 3 - Application Bootstrap

## Overview

Phase 3 establishes the foundational application bootstrap layer for the NestJS backend.

The goal of this phase is to configure the application startup process, database integration, security middleware, logging, validation, API documentation, and health monitoring.

At the end of this phase, the NestJS application can:

* Start successfully
* Connect to PostgreSQL
* Expose Swagger documentation
* Apply security headers
* Enable CORS
* Validate incoming requests globally
* Log requests using Pino
* Provide a health check endpoint

---

## Features Implemented

### ConfigModule

Global configuration management is enabled using:

* @nestjs/config
* Environment variables
* Centralized configuration files

Loaded configurations:

* app.config.ts
* database.config.ts
* jwt.config.ts

---

### TypeORM Integration

Database connection is configured using:

* PostgreSQL
* TypeORM
* ConfigService
* Async initialization

Configuration includes:

* Host
* Port
* Username
* Password
* Database Name

Database synchronization remains disabled:

```ts
synchronize: false
```

to ensure migration-driven schema management.

---

### Helmet Security

Helmet middleware is enabled globally.

Provides protection through security headers such as:

* X-Content-Type-Options
* X-Frame-Options
* Content-Security-Policy
* Referrer-Policy

---

### CORS Configuration

Cross-Origin Resource Sharing (CORS) is enabled.

Allowed origin:

```env
FRONTEND_URL=http://localhost:3000
```

Credentials support is enabled for future authenticated requests.

---

### Global ValidationPipe

A global validation pipeline is configured.

Features:

* DTO validation
* Automatic transformation
* Payload sanitization
* Unknown property rejection

Configuration:

```ts
whitelist: true
forbidNonWhitelisted: true
transform: true
```

---

### Pino Logger

Structured request logging is configured using:

* nestjs-pino
* pino
* pino-pretty

Provides:

* HTTP request logs
* Response logs
* Error logs
* Development-friendly output

---

### Swagger Documentation

Swagger UI is configured for API documentation.

Features:

* API Explorer
* Request/Response Schemas
* JWT Bearer Authentication Support

Swagger URL:

```text
http://localhost:3001/api/docs
```

Bearer authentication is preconfigured for future FastAPI-issued JWT integration.

---

### Health Check Endpoint

A dedicated health module is implemented.

Endpoint:

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "nestjs-backend"
}
```

Purpose:

* Service monitoring
* Docker health checks
* Load balancer verification
* Deployment validation

---

## Files Created

```text
src/

├── health/
│   ├── health.controller.ts
│   └── health.module.ts
```

---

## Files Updated

```text
src/

├── main.ts
├── app.module.ts
```

---

## Files Removed

Default NestJS starter files were removed:

```text
src/

├── app.controller.ts
├── app.controller.spec.ts
└── app.service.ts
```

---

## Verification

Start the application:

```bash
npm run start:dev
```

Verify health endpoint:

```http
GET http://localhost:3001/health
```

Verify Swagger:

```text
http://localhost:3001/api/docs
```

Verify database connectivity:

Application startup should complete successfully without TypeORM connection errors.

---

## Phase 3 Completion Status

Completed:

* ConfigModule
* TypeOrmModule
* Helmet
* CORS
* ValidationPipe
* Pino Logger
* Swagger
* Health Endpoint

Result:

The NestJS backend is successfully bootstrapped and ready for authentication integration and feature module development.

---

# Phase 4 - Authentication Foundation

## Overview

Phase 4 establishes the authentication and authorization foundation for the NestJS Backend.

NestJS does not own authentication. Authentication remains fully managed by the FastAPI Backend.

NestJS validates JWT access tokens issued by FastAPI and provides role-based access control (RBAC) utilities that will be used by all future modules such as Tasks, Categories, Tags, Notifications, Analytics, and Activity Logs.

---

## Objectives

Implemented:

* JWT Authentication Strategy
* JWT Authentication Guard
* Role-Based Authorization Guard
* Roles Decorator
* Current User Decorator
* Shared JWT Payload Interface
* Shared Role Enumeration
* FastAPI JWT Validation

---

## Authentication Architecture

Authentication ownership:

```text
FastAPI
│
├── Register User
├── Login User
├── Generate JWT
└── Manage Credentials

        │

        ▼

Frontend
        │
        ├── Calls FastAPI APIs
        └── Calls NestJS APIs

        ▼

NestJS
│
├── Validate JWT
├── Extract User Information
└── Enforce Authorization Rules
```

NestJS never creates, refreshes, or manages tokens.

---

## JWT Contract

NestJS validates JWTs generated by FastAPI.

Expected payload:

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

Validation rules:

* Signature Validation
* Issuer Validation
* Audience Validation
* Expiration Validation

---

## Folder Structure

```text
src/

├── auth/
│
│   ├── auth.module.ts
│
│   ├── guards/
│   │   ├── jwt-auth.guard.ts
│   │   └── roles.guard.ts
│
│   └── strategies/
│       └── jwt.strategy.ts
│
├── common/
│
│   ├── constants/
│   │   └── roles.enum.ts
│
│   ├── decorators/
│   │   ├── current-user.decorator.ts
│   │   └── roles.decorator.ts
│
│   └── interfaces/
│       └── jwt-payload.interface.ts
```

---

## Implemented Components

### AuthModule

Registers Passport and JWT authentication components.

Responsibilities:

* Authentication configuration
* JWT strategy registration
* Guard exports

---

### JwtStrategy

Validates FastAPI-issued JWTs.

Checks:

* JWT Signature
* JWT Issuer
* JWT Audience
* JWT Expiration

Returns authenticated user payload to request context.

---

### JwtAuthGuard

Protects endpoints that require authentication.

Example:

```ts
@UseGuards(JwtAuthGuard)
@Get()
findAll() {}
```

---

### RolesGuard

Provides role-based authorization.

Example:

```ts
@Roles(Role.ADMIN)
@UseGuards(
  JwtAuthGuard,
  RolesGuard,
)
@Get('admin')
adminOnly() {}
```

---

### Roles Decorator

Declares allowed roles for a route.

Example:

```ts
@Roles(Role.ADMIN)
```

---

### CurrentUser Decorator

Extracts authenticated user information from the request.

Example:

```ts
@Get('profile')
profile(
  @CurrentUser() user: JwtPayload,
) {
  return user;
}
```

---

### Role Enum

Supported roles:

```ts
ADMIN
USER
```

Future roles can be added without modifying existing modules.

---

### JWT Payload Interface

Defines the shared authentication contract used across the application.

Properties:

```ts
sub
email
role
iss
aud
type
iat
exp
```

---

## Security Features

Implemented security checks:

* JWT Signature Verification
* JWT Expiration Validation
* Issuer Validation
* Audience Validation
* Authentication Guard
* Authorization Guard
* RBAC Foundation

---

## Swagger Integration

Swagger authentication support was already configured in Phase 3.

Authentication can be tested through:

```text
http://localhost:3001/api/docs
```

Use:

```text
Authorize
Bearer <FastAPI JWT Token>
```

to test protected APIs.

---

## Testing Checklist

Build Verification:

```bash
npm run build
```

Run Application:

```bash
npm run start:dev
```

Health Check:

```http
GET /health
```

Expected Response:

```json
{
  "status": "ok",
  "service": "nestjs-backend"
}
```

Authentication Tests:

* Valid JWT → 200 OK
* Missing JWT → 401 Unauthorized
* Expired JWT → 401 Unauthorized
* Invalid Issuer → 401 Unauthorized
* Invalid Audience → 401 Unauthorized

Authorization Tests:

* ADMIN accessing ADMIN route → Allowed
* USER accessing ADMIN route → Forbidden (403)

---

## Phase 4 Deliverables

Completed:

* AuthModule
* JwtStrategy
* JwtAuthGuard
* RolesGuard
* Roles Decorator
* CurrentUser Decorator
* Role Enum
* JWT Payload Interface
* FastAPI JWT Validation
* RBAC Foundation

---

# Phase 5 - Tasks Module

## Overview

Phase 5 introduces the first business module of the NestJS Backend:

```text
Tasks Module
```

This module is responsible for managing user tasks and serves as the foundation for future productivity features such as Categories, Tags, Notifications, Analytics, and Activity Logs.

The module is fully protected using JWT authentication and enforces task ownership using the user identity provided by the FastAPI-issued access token.

---

# Features Implemented

## Task Entity

Implemented a production-ready Task entity with:

* UUID Primary Key
* Title
* Description
* Status
* Priority
* Due Date
* User Ownership
* Created Timestamp
* Updated Timestamp

---

## JWT Ownership Enforcement

Every task belongs to a specific user.

Ownership is determined using:

```ts
user.sub
```

from the validated FastAPI JWT payload.

Example:

```json
{
  "sub": "1",
  "email": "user@example.com",
  "role": "USER"
}
```

This ensures:

* Users can only access their own tasks
* Cross-user data access is prevented
* Multi-tenant task isolation is enforced

---

## CRUD Operations

Implemented:

### Create Task

```http
POST /api/tasks
```

### Get User Tasks

```http
GET /api/tasks
```

### Get Task By ID

```http
GET /api/tasks/:id
```

### Update Task

```http
PATCH /api/tasks/:id
```

### Delete Task

```http
DELETE /api/tasks/:id
```

---

# Pagination

Supported query parameters:

```http
GET /api/tasks?page=1&limit=10
```

Response includes:

* Data
* Total Records
* Current Page
* Page Size
* Total Pages

---

# Filtering

Tasks can be filtered by:

## Status

```http
GET /api/tasks?status=TODO
```

Supported values:

* TODO
* IN_PROGRESS
* COMPLETED
* CANCELLED

---

## Priority

```http
GET /api/tasks?priority=HIGH
```

Supported values:

* LOW
* MEDIUM
* HIGH
* URGENT

---

# Search

Search by task title:

```http
GET /api/tasks?search=nestjs
```

---

# Sorting

Supported query parameters:

```http
GET /api/tasks?sortBy=createdAt&sortOrder=DESC
```

Example:

```http
GET /api/tasks?sortBy=priority&sortOrder=ASC
```

---

# Swagger Documentation

All endpoints are documented using NestJS Swagger.

Swagger URL:

```text
http://localhost:3001/api/docs
```

Authentication:

```text
Bearer Token (FastAPI JWT)
```

---

# Folder Structure

```text
src/tasks/

├── controllers/
│   └── tasks.controller.ts
│
├── services/
│   └── tasks.service.ts
│
├── entities/
│   └── task.entity.ts
│
├── dto/
│   ├── create-task.dto.ts
│   ├── update-task.dto.ts
│   ├── task-query.dto.ts
│   └── task-response.dto.ts
│
├── enums/
│   ├── task-priority.enum.ts
│   └── task-status.enum.ts
│
└── tasks.module.ts
```

---

# Database Schema

Table:

```sql
tasks
```

Columns:

| Column      | Type         |
| ----------- | ------------ |
| id          | UUID         |
| title       | VARCHAR(255) |
| description | TEXT         |
| status      | ENUM         |
| priority    | ENUM         |
| dueDate     | TIMESTAMP    |
| userId      | VARCHAR(100) |
| createdAt   | TIMESTAMP    |
| updatedAt   | TIMESTAMP    |

---

# Security

Protected by:

```ts
JwtAuthGuard
```

JWT Validation:

* Signature Validation
* Issuer Validation
* Audience Validation
* Expiration Validation

RBAC foundation is available through:

```ts
RolesGuard
```

for future authorization requirements.

---

# Migration

Migration created:

```text
src/database/migrations/00-create-tasks.ts
```

Apply migrations:

```bash
npm run migration:run
```

Rollback:

```bash
npm run migration:revert
```

---

# Future Enhancements

Phase 5 intentionally excludes:

* Categories
* Tags
* Task-Tag Relations
* Notifications
* Analytics
* Activity Logs

These will be implemented in later phases.

---

# Phase 5 Completion

Completed:

* Task Entity
* DTO Validation
* Swagger Documentation
* CRUD APIs
* JWT Protection
* Ownership Enforcement
* Pagination
* Filtering
* Search
* Sorting
* TypeORM Integration
* PostgreSQL Migration

---

# Phase 6 - Categories Module

## Overview

Phase 6 introduces the Categories Module to the Team Productivity Platform.

Categories allow users to organize tasks into logical groups such as:

* Work
* Personal
* Learning
* Health
* Shopping

Each category belongs to a specific authenticated user and is protected through JWT-based ownership enforcement.

The module follows the same architecture and security patterns established in the Tasks Module.

---

## Features Implemented

### Category Entity

Implemented a Category entity with:

* UUID Primary Key
* Name
* Description
* Color
* User Ownership
* Created Timestamp
* Updated Timestamp

```text
Category
├── id
├── name
├── description
├── color
├── userId
├── createdAt
└── updatedAt
```

---

### CRUD Operations

Implemented complete Category CRUD functionality.

Endpoints:

```http
POST   /api/categories
GET    /api/categories
GET    /api/categories/:id
PATCH  /api/categories/:id
DELETE /api/categories/:id
```

---

### JWT Ownership Enforcement

Categories are owned by authenticated users.

Ownership is derived from:

```ts
userId = JWT.sub
```

Users can:

* Create their own categories
* View their own categories
* Update their own categories
* Delete their own categories

Users cannot access categories belonging to other users.

---

### Pagination

Supported query parameters:

```http
GET /api/categories?page=1&limit=10
```

Response includes:

```json
{
  "data": [],
  "total": 0,
  "page": 1,
  "limit": 10,
  "totalPages": 0
}
```

---

### Search

Supported category name search:

```http
GET /api/categories?search=work
```

Search is case-insensitive.

---

### Sorting

Supported sorting parameters:

```http
GET /api/categories?sortBy=createdAt&sortOrder=DESC
```

Available fields:

* createdAt
* updatedAt
* name

---

### Swagger Documentation

All endpoints include Swagger documentation.

Swagger URL:

```text
http://localhost:3001/api/docs
```

Categories are available under:

```text
Categories
```

section.

---

## Database Changes

### New Table

```text
categories
```

Columns:

```text
id
name
description
color
userId
createdAt
updatedAt
```

---

### Indexes

Created:

```text
IDX_CATEGORY_USER_ID
```

Used for efficient ownership filtering.

---

## Task ↔ Category Relationship

Implemented:

```text
Category (1)
      |
      |
      └─────> (Many) Tasks
```

### Task Entity Updates

Added:

```text
categoryId
```

Relationship:

```ts
@ManyToOne(() => Category)
```

---

### Category Entity Updates

Added:

```ts
@OneToMany(() => Task)
```

allowing future task-category navigation.

---

## Folder Structure

```text
src/categories/

├── controllers/
│   └── categories.controller.ts
│
├── services/
│   └── categories.service.ts
│
├── entities/
│   └── category.entity.ts
│
├── dto/
│   ├── create-category.dto.ts
│   ├── update-category.dto.ts
│   ├── category-query.dto.ts
│   └── category-response.dto.ts
│
└── categories.module.ts
```

---

## Migration

Created:

```text
src/database/migrations/01-create-categories.ts
```

Responsibilities:

* Create categories table
* Create ownership index
* Add categoryId column to tasks table
* Create Task → Category foreign key

---

## Security

Protected using:

```ts
JwtAuthGuard
```

All Category endpoints require a valid JWT issued by FastAPI.

JWT validation includes:

* Signature Validation
* Issuer Validation
* Audience Validation
* Expiration Validation

---

## Result

The Categories Module is fully integrated into the NestJS backend and provides task organization capabilities through a secure user-owned category system.

This completes Phase 6 of the NestJS backend roadmap.

---

## Phase 7 - Tags Module

### Overview

The Tags Module introduces reusable labels that can be attached to tasks.

Tags allow users to organize, filter, and categorize tasks beyond a single category relationship.

Examples:

```text
Backend
Frontend
Bug
Feature
Research
Urgent
Personal
Work
```

---

### Folder Structure

```text
src/tags/

├── controllers/
│   └── tags.controller.ts
│
├── services/
│   └── tags.service.ts
│
├── entities/
│   └── tag.entity.ts
│
├── dto/
│   ├── create-tag.dto.ts
│   ├── update-tag.dto.ts
│   ├── tag-query.dto.ts
│   └── tag-response.dto.ts
│
└── tags.module.ts
```

---

### Database Migrations

```text
src/database/migrations/

02-create-tags.ts
03-create-task-tags.ts
```

---

### Tag Entity

The Tag entity contains:

```text
id
name
color
userId
createdAt
updatedAt
```

Ownership is enforced through:

```ts
userId = JWT.sub
```

---

### Task ↔ Tag Relationship

Implemented using a many-to-many relationship.

```text
Task (Many)
      ↔
Tag (Many)
```

Database structure:

```text
tasks
tags
task_tags
```

The junction table stores task and tag associations.

```text
taskId
tagId
```

Example:

```text
Task:
Fix Login Bug

Tags:
Backend
Bug
Urgent
```

---

### Tag CRUD APIs

Create Tag

```http
POST /api/tags
```

Get User Tags

```http
GET /api/tags
```

Get Tag By ID

```http
GET /api/tags/:id
```

Update Tag

```http
PATCH /api/tags/:id
```

Delete Tag

```http
DELETE /api/tags/:id
```

---

### Features

Implemented:

* JWT Protected Endpoints
* Ownership Enforcement
* Pagination
* Search
* Sorting
* Swagger Documentation
* Tag CRUD Operations
* Many-to-Many Task ↔ Tag Relationship
* Task Tag Assignment
* Task Tag Updates
* Task Tag Retrieval

---

### Task Module Enhancements

The Tasks Module was updated to support tags.

#### Create Task

```json
{
  "title": "Fix Login Bug",
  "priority": "HIGH",
  "tagIds": [
    "tag-uuid-1",
    "tag-uuid-2"
  ]
}
```

#### Update Task

```json
{
  "tagIds": [
    "tag-uuid-3",
    "tag-uuid-4"
  ]
}
```

#### Task Response

```json
{
  "id": "...",
  "title": "Fix Login Bug",
  "tags": [
    {
      "id": "...",
      "name": "Backend"
    },
    {
      "id": "...",
      "name": "Urgent"
    }
  ]
}
```

---

### Security

All endpoints require authentication.

```ts
JwtAuthGuard
```

Tag ownership is enforced by validating:

```ts
userId === JWT.sub
```

Users can only access and manage their own tags.

---

### FastAPI Integration

No FastAPI changes were required.

FastAPI remains responsible for:

```text
Authentication
Notes
Admin Notes
Health
```

NestJS continues validating FastAPI-issued JWTs.

---

### Frontend Impact

The task creation and update forms now support tag assignment.

Example:

```text
Title
Description
Priority
Status
Category

Tags
☑ Backend
☑ Bug
☑ Urgent
☐ Research
```

Tasks can display multiple labels:

```text
Fix Login Bug

[Backend]
[Bug]
[Urgent]
```

---

# Phase 8 - Activity Logs Module

## Overview

The Activity Logs Module provides a complete audit trail system for the Team Productivity Platform.

Every important user action is automatically recorded and can be retrieved later for:

* Activity Feeds
* User History
* Analytics
* Notifications
* Audit Tracking
* Monitoring

The module is read-only from the API perspective.

Activity logs are generated internally by the application whenever users create, update, or delete resources.

---

## Folder Structure

```text
src/activity-logs/

├── controllers/
│   └── activity-logs.controller.ts
│
├── services/
│   └── activity-logs.service.ts
│
├── entities/
│   └── activity-log.entity.ts
│
├── dto/
│   ├── activity-log-query.dto.ts
│   └── activity-log-response.dto.ts
│
├── enums/
│   ├── activity-action.enum.ts
│   └── activity-entity-type.enum.ts
│
└── activity-logs.module.ts
```

---

## Database Migration

```text
src/database/migrations/

04-create-activity-logs.ts
```

Creates:

```text
activity_logs
```

---

## Activity Log Entity

### Columns

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| action     | ENUM      |
| entityType | ENUM      |
| entityId   | UUID      |
| metadata   | JSONB     |
| userId     | VARCHAR   |
| createdAt  | TIMESTAMP |

---

### Example Record

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "action": "TASK_CREATED",
  "entityType": "TASK",
  "entityId": "550e8400-e29b-41d4-a716-446655440001",
  "metadata": {
    "title": "Complete NestJS Phase 8"
  },
  "userId": "1",
  "createdAt": "2026-06-13T08:00:00.000Z"
}
```

---

## Activity Actions

### Task Events

```text
TASK_CREATED
TASK_UPDATED
TASK_DELETED
```

### Category Events

```text
CATEGORY_CREATED
CATEGORY_UPDATED
CATEGORY_DELETED
```

### Tag Events

```text
TAG_CREATED
TAG_UPDATED
TAG_DELETED
```

---

## Entity Types

```text
TASK
CATEGORY
TAG
```

---

## Automatic Activity Tracking

### Tasks

Activities generated automatically for:

```text
Create Task
Update Task
Delete Task
Convert Note → Task
```

---

### Categories

Activities generated automatically for:

```text
Create Category
Update Category
Delete Category
```

---

### Tags

Activities generated automatically for:

```text
Create Tag
Update Tag
Delete Tag
```

---

## API Endpoints

### Get User Activity Logs

```http
GET /api/activity-logs
```

Query Parameters:

```http
?page=1
&limit=10
&action=TASK_CREATED
&entityType=TASK
&sortBy=createdAt
&sortOrder=DESC
```

---

### Get Activity Log By ID

```http
GET /api/activity-logs/:id
```

---

## Security

All endpoints require authentication.

```http
Authorization: Bearer <token>
```

Protection:

```text
JWT Authentication
Ownership Enforcement
User Isolation
```

Users can only access their own activity logs.

---

## Pagination

Response Format:

```json
{
  "data": [],
  "total": 25,
  "page": 1,
  "limit": 10,
  "totalPages": 3
}
```

---

## Filtering

Supported Filters:

```text
action
entityType
```

Examples:

```http
GET /api/activity-logs?action=TASK_CREATED
```

```http
GET /api/activity-logs?entityType=CATEGORY
```

---

## Sorting

Supported Parameters:

```http
sortBy
sortOrder
```

Example:

```http
GET /api/activity-logs?sortBy=createdAt&sortOrder=DESC
```

---

## Database Indexes

```text
IDX_ACTIVITY_USER_ID
IDX_ACTIVITY_ACTION
IDX_ACTIVITY_ENTITY_TYPE
IDX_ACTIVITY_ENTITY_ID
IDX_ACTIVITY_CREATED_AT
```

These indexes improve:

```text
Filtering
Pagination
Analytics Queries
Audit Queries
Activity Feed Performance
```

---

## Integration Points

The Activity Logs Module is integrated with:

```text
Tasks Module
Categories Module
Tags Module
```

via:

```ts
ActivityLogsService
```

---

# Phase 9 - Notifications Module

## Overview

Phase 9 introduces the Notifications Module for the Team Productivity Platform.

This module provides in-app notifications that allow users to stay informed about important actions and events occurring within the system.

Notifications are user-specific and protected through JWT authentication.

---

## Folder Structure

```text
src/notifications/

├── controllers/
│   └── notifications.controller.ts
│
├── services/
│   └── notifications.service.ts
│
├── entities/
│   └── notification.entity.ts
│
├── dto/
│   ├── notification-query.dto.ts
│   ├── notification-response.dto.ts
│   └── mark-notification-read.dto.ts
│
├── enums/
│   ├── notification-type.enum.ts
│   └── notification-status.enum.ts
│
└── notifications.module.ts
```

---

## Database Migration

```text
05-create-notifications.ts
```

Creates:

```text
notifications
```

Table Columns:

```text
id
title
message
type
status
userId
createdAt
updatedAt
```

Indexes:

```text
IDX_NOTIFICATION_USER_ID
IDX_NOTIFICATION_STATUS
IDX_NOTIFICATION_TYPE
```

---

## Notification Types

Supported notification types:

```text
TASK_DUE
TASK_OVERDUE
TASK_COMPLETED
CATEGORY_UPDATED
TAG_ASSIGNED
SYSTEM
```

---

## Notification Status

```text
UNREAD
READ
```

---

## Features

Implemented:

```text
Notification Persistence
Notification Listing
Notification Filtering
Notification Pagination
Notification Sorting
Notification Ownership Enforcement
JWT Protection
Mark Notification As Read
Mark All Notifications As Read
```

---

## Automatic Notification Generation

Implemented integrations:

### Task Notifications

Generated when:

```text
Task Status Changes To COMPLETED
```

Notification:

```text
TASK_COMPLETED
```

---

### Category Notifications

Generated when:

```text
Category Updated
```

Notification:

```text
CATEGORY_UPDATED
```

---

### Tag Assignment Notifications

Generated when:

```text
Tags Assigned To Task
```

Notification:

```text
TAG_ASSIGNED
```

---

## API Endpoints

### Get User Notifications

```http
GET /api/notifications
```

Query Parameters:

```text
page
limit
status
type
sortBy
sortOrder
```

---

### Get Notification By ID

```http
GET /api/notifications/:id
```

---

### Mark Notification As Read

```http
PATCH /api/notifications/:id/read
```

---

### Mark All Notifications As Read

```http
PATCH /api/notifications/read-all
```

---

## Security

All notification endpoints require authentication.

```text
JwtAuthGuard
```

Notifications are restricted to the authenticated user.

Ownership validation is enforced using:

```ts
userId = JWT.sub
```

Users cannot access notifications belonging to other users.

---

## Integration Points

Integrated Modules:

```text
Tasks Module
Categories Module
```

Notification creation occurs through:

```ts
NotificationsService.create()
```

---

## Phase 10 – Analytics Module 

Implemented:

- Analytics Module
- Analytics Controller
- Analytics Service
- Analytics DTOs

Features:

- Dashboard Statistics
- Task Status Analytics
- Task Priority Analytics
- Productivity Metrics
- Completion Rate Calculation
- User Ownership Enforcement
- JWT Protection
- Swagger Documentation

Endpoints:

GET /api/analytics/overview

GET /api/analytics/tasks/status

GET /api/analytics/tasks/priority

GET /api/analytics/productivity

Analytics Metrics:

- Total Tasks
- Completed Tasks
- Pending Tasks
- Categories Count
- Tags Count
- Notifications Count
- Task Status Distribution
- Task Priority Distribution
- Completion Rate

---

# Phase 11 – Testing

## Overview

This phase focuses on validating the NestJS backend through unit tests, controller tests, and integration tests. The goal is to ensure business logic correctness, API reliability, authentication behavior, and database interactions.

---

## Testing Stack

* Jest
* Supertest
* NestJS Testing Module
* TypeORM Test Database
* Mock Repositories
* Mock JWT Authentication

---

## Unit Tests

### Authentication

Tested Components:

* JwtStrategy
* JwtAuthGuard
* RolesGuard

Covered Scenarios:

* Valid JWT payload validation
* Invalid JWT rejection
* Role authorization checks
* User extraction from request

---

### Services

Tested Services:

* TasksService
* CategoriesService
* TagsService
* NotificationsService
* AnalyticsService

Covered Scenarios:

* Create operations
* Read operations
* Update operations
* Delete operations
* Ownership enforcement
* Pagination logic
* Search functionality
* Analytics calculations

---

## Controller Tests

Tested Controllers:

* TasksController
* CategoriesController
* TagsController
* NotificationsController
* AnalyticsController

Covered Scenarios:

* Request validation
* Successful responses
* Error responses
* Authorization checks
* Query parameter handling

---

## Integration Tests

### Tasks Module

Verified:

* Task creation
* Task retrieval
* Task update
* Task deletion

### Categories Module

Verified:

* Category CRUD operations
* Ownership restrictions

### Tags Module

Verified:

* Tag CRUD operations
* Search and pagination

### Notifications Module

Verified:

* Notification retrieval
* Mark as read
* Mark all as read

---

## Test Results

```text
Test Suites: 17 Passed
Tests: 54 Passed
Failures: 0
```

---

## Running Tests

Run all tests:

```bash
npm run test
```

Run tests in watch mode:

```bash
npm run test:watch
```

Run coverage:

```bash
npm run test:cov
```

Run e2e tests:

```bash
npm run test:e2e
```

---

## Outcome

All major business modules, authentication mechanisms, analytics endpoints, and notification workflows were successfully validated.

---

# Phase 12 – Dockerization

## Overview

This phase containerizes the NestJS backend and PostgreSQL database to ensure consistent deployment and local development environments.

---

## Components

### Dockerfile

Used to build the NestJS application container.

Responsibilities:

* Install dependencies
* Build TypeScript application
* Expose application port
* Start NestJS server

---

### Docker Compose

Provides multi-container orchestration for:

* NestJS Backend
* PostgreSQL Database

---

## Container Architecture

```text
+----------------------+
| NestJS Backend       |
| Port: 3001           |
+----------+-----------+
           |
           |
           v
+----------------------+
| PostgreSQL           |
| Port: 5432           |
+----------------------+
```

---

## Dockerfile

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3001

CMD ["node", "dist/main.js"]
```

---

## Docker Compose

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:17-alpine
    container_name: team-productivity-postgres

    restart: unless-stopped

    environment:
      POSTGRES_DB: productivity_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

  nestjs-backend:
    build: .
    container_name: team-productivity-nestjs

    restart: unless-stopped

    depends_on:
      - postgres

    ports:
      - "3001:3001"

    env_file:
      - .env

volumes:
  postgres_data:
```

---

## Docker Commands

Build containers:

```bash
docker compose build
```

Start containers:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f
```

Stop containers:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

## Verification

Check running containers:

```bash
docker ps
```

Expected Containers:

```text
team-productivity-postgres
team-productivity-nestjs
```

Verify API:

```http
GET http://localhost:3001/health
```

Expected Response:

```json
{
  "status": "ok",
  "service": "nestjs-backend"
}
```

---

## Outcome

The NestJS backend and PostgreSQL database can be deployed using Docker with a single command, providing a reproducible and portable development environment.


