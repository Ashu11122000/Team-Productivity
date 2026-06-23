# Team Productivity Platform

> A modern productivity ecosystem that combines Notes, Tasks, Projects, Team Collaboration, Knowledge Management, Analytics, Notifications, and Activity Tracking into a single unified platform.

---

# Vision

The Team Productivity Platform aims to become a centralized productivity ecosystem for individuals, startups, freelancers, students, and organizations.

The platform combines the strengths of:

* Notion (Knowledge Management)
* Todoist (Task Management)
* Trello (Kanban Boards)
* Jira (Project Tracking)
* Slack (Collaboration & Activity Awareness)

into a single scalable platform.

The primary goal is to eliminate fragmented workflows by providing one place where users can:

* Create and manage notes
* Organize tasks
* Track projects
* Collaborate with teams
* Monitor productivity
* Access knowledge resources
* Receive notifications
* Analyze performance

while maintaining high performance, scalability, and extensibility.

---

# Problem Statement

Modern individuals, students, freelancers, startups, and organizations use multiple disconnected tools to manage their daily work.

Examples:

| Purpose           | Common Tool   |
| ----------------- | ------------- |
| Notes             | Notion        |
| Tasks             | Todoist       |
| Projects          | Trello / Jira |
| Communication     | Slack         |
| Documentation     | Confluence    |
| Knowledge Storage | Various Apps  |

Because these systems are separated:

* Information becomes fragmented
* Productivity decreases
* Context switching increases
* Team collaboration becomes difficult
* Tracking progress becomes challenging
* Important tasks are often missed
* Knowledge management becomes inefficient

Many existing productivity tools are:

* Too simple and lack advanced features
* Too complex for small teams
* Expensive for startups and students
* Difficult to customize
* Poorly optimized for performance

There is a need for a modern, scalable, high-performance productivity platform that combines note-taking, task management, project organization, analytics, and collaboration features into a unified ecosystem.

---

# Proposed Solution

The Team Productivity Platform is a full-stack productivity ecosystem designed to help individuals and teams organize their work efficiently through a centralized platform.

The platform provides:

* User Authentication
* Note Management
* Task Management
* Project Organization
* Categories and Tags
* Team Collaboration
* Activity Tracking
* Notifications
* Analytics & Productivity Insights
* Knowledge Management
* Mobile & Web Access

The system follows an API-first architecture powered by:

* FastAPI Microservice
* NestJS Microservice
* PostgreSQL
* Next.js Web Application
* Flutter Mobile Application

All clients consume the same backend APIs.

---

# Core Objectives

## Authentication & Security

Provide secure authentication and authorization mechanisms.

### Traditional Authentication

* User Registration
* Login
* Logout
* Refresh Token
* Forgot Password
* Reset Password
* Email Verification

### Social Authentication

* Google Sign In
* Google Sign Up

### Session Management

* Remember Me
* Persistent Login
* Active Sessions
* Logout From All Devices

### Security Features

* JWT Authentication
* Refresh Tokens
* Password Hashing (bcrypt)
* Rate Limiting
* RBAC
* Permission-Based Access Control
* Audit Logging

---

## User Productivity

Enable users to:

* Create Notes
* Organize Tasks
* Track Progress
* Manage Deadlines
* Monitor Productivity
* View Analytics
* Manage Personal Workflows

---

## Knowledge Management

Enable users to:

* Store Personal Notes
* Create Project Documentation
* Maintain Team Knowledge Bases
* Search Information Efficiently
* Link Knowledge With Tasks

---

## Task Organization

Enable users to:

* Create Tasks
* Assign Tasks
* Categorize Tasks
* Add Tags
* Set Priorities
* Track Progress
* Convert Notes Into Tasks
* Manage Deadlines

---

## Collaboration

Enable teams to:

* Collaborate on Projects
* Share Information
* Track Activities
* Manage Workspaces
* Discuss Through Comments
* Receive Notifications

---

## Analytics

Provide actionable insights such as:

* Task Completion Rate
* Productivity Trends
* Team Performance
* Activity History
* Workload Distribution
* Project Progress Reports

---

## Cross Platform Support

Provide seamless access through:

### Web Application

* Next.js
* Responsive UI
* Optimized Performance

### Mobile Application

* Flutter
* Native Experience
* Push Notifications

Both applications consume the same APIs.

---

# Core Features

## Authentication System

### User Management

* Register
* Login
* Logout
* Profile Management
* Email Verification
* Password Reset

### Session Control

* Remember Me
* Active Sessions
* Device Management
* Logout Everywhere

---

## Notes Management

### Features

* Create Notes
* Update Notes
* Archive Notes
* Delete Notes
* Search Notes
* Categorize Notes
* Tag Notes

### Rich Text Support

* Headings
* Lists
* Checklists
* Tables
* Code Blocks
* Images
* Links
* Markdown

---

## Task Management

### Features

* Create Tasks
* Update Tasks
* Delete Tasks
* Archive Tasks
* Assign Tasks
* Track Progress

### Task Priorities

* Low
* Medium
* High
* Critical

### Task Status

* Backlog
* Todo
* In Progress
* Review
* Completed
* Cancelled

---

## Subtasks

Example:

Build Dashboard

├── Create UI
├── Connect APIs
└── Testing

Database Relationship:

```text
tasks
 └── parent_task_id
```

---

## Due Dates & Reminders

Each task supports:

* Start Date
* Due Date
* Reminder Date

Example:

```text
Task: Finish Dashboard

Start Date:
20 June

Due Date:
25 June

Reminder:
24 June 10:00 AM
```

---

## Recurring Tasks

Examples:

* Daily Standup
* Weekly Report
* Monthly Review

Fields:

```text
is_recurring
repeat_type
next_due_date
```

---

## Categories & Tags

Help users organize work efficiently.

### Categories

Examples:

* Personal
* Work
* Study
* Project

### Tags

Examples:

* Frontend
* Backend
* Bug
* Feature
* Urgent

---

## Bookmarks & Favorites

Users can bookmark:

* Notes
* Tasks
* Projects

Examples:

* Favorite Project
* Favorite Task
* Favorite Note

Database Table:

```text
favorites
```

---

# Role Based Access Control (RBAC)

The platform supports Role-Based Access Control.

## Roles

### Admin

Can:

* Manage Users
* Manage Projects
* Assign Managers
* Manage Workspaces
* View Organization Analytics

---

### Manager

Can:

* Create Projects
* Assign Tasks
* Manage Teams
* Manage Members
* View Team Analytics

---

### Team Lead

Can:

* Manage Team Tasks
* Review Work
* Update Sprint Progress
* Monitor Team Performance

---

### Employee

Can:

* Create Notes
* Manage Assigned Tasks
* Comment
* Upload Attachments
* Participate In Projects

---

# Permission System

The system supports fine-grained permissions.

Examples:

```text
tasks.create
tasks.update
tasks.delete

projects.create
projects.update
projects.archive

users.manage

analytics.view
```

Database Structure:

```text
roles

permissions

role_permissions

user_roles
```

---

# Workspace Management

A company can have multiple workspaces.

Example:

Company
├── Engineering
├── Marketing
├── HR
└── Finance

Database Tables:

```text
workspaces

workspace_members
```

Workspace Features:

* Create Workspace
* Invite Members
* Manage Roles
* Workspace Analytics
* Workspace Settings

---

# Team Management

Teams exist inside workspaces.

Examples:

* Backend Team
* Frontend Team
* Mobile Team
* QA Team
* DevOps Team

Database Tables:

```text
teams

team_members
```

Features:

* Create Team
* Add Members
* Remove Members
* Assign Team Lead
* Team Analytics

---

# Projects

Projects are used to organize work and track progress.

Features:

* Create Project
* Update Project
* Archive Project
* Assign Members
* Track Progress
* Set Deadlines
* Monitor Status

Project Status:

* Planning
* Active
* On Hold
* Completed
* Archived

Database Tables:

```text
projects

project_members
```
---

# Comments System

The platform supports threaded discussions across multiple resources.

Users can collaborate directly within:

* Tasks
* Projects
* Notes

This reduces dependency on external communication tools and keeps conversations close to the work being discussed.

---

## Features

### Task Comments

Users can:

* Add comments
* Reply to comments
* Mention team members
* Edit comments
* Delete comments

---

### Project Comments

Used for:

* Project discussions
* Status updates
* Requirement clarifications
* Team communication

---

### Note Comments

Used for:

* Knowledge reviews
* Documentation feedback
* Collaborative note-taking

---

### Mentions

Users can mention others using:

```text
@username
```

Mentioned users receive notifications.

---

## Database Tables

```text
comments

comment_mentions
```

---

# Attachments

The platform supports file attachments across multiple entities.

Attachments can be added to:

* Notes
* Tasks
* Projects
* Comments

---

## Supported File Types

Documents

* PDF
* DOC
* DOCX
* XLS
* XLSX
* PPT
* PPTX

Images

* PNG
* JPG
* JPEG
* SVG
* WEBP

Archives

* ZIP
* RAR

---

## File Upload Rules

Maximum File Size:

```text
25 MB
```

Future support:

```text
Cloud Storage
AWS S3
MinIO
CDN Delivery
```

---

## Database Tables

```text
attachments
```

---

# Notifications

The platform provides a centralized notification system.

Users receive notifications when important events occur.

---

## Notification Types

### Task Notifications

* Task Assigned
* Task Updated
* Task Completed
* Task Reassigned

---

### Comment Notifications

* Comment Mention
* Reply Received

---

### Project Notifications

* Project Updated
* Project Status Changed
* Project Deadline Updated

---

### Deadline Notifications

* Upcoming Deadline
* Overdue Task Reminder

---

## Delivery Channels

### In-App Notifications

Supported initially.

### Push Notifications

Future Mobile Support.

### Email Notifications

Future Release.

---

## Database Table

```text
notifications
```

---

# Notification Preferences

Users can customize notifications.

Examples:

### Enable / Disable

* Email Notifications
* Push Notifications
* In-App Notifications
* Mention Notifications
* Deadline Reminders

---

## Benefits

Reduces notification fatigue while keeping users informed.

---

# Activity Feed

The platform includes a real-time activity feed.

Users can see what is happening across their workspace.

Examples:

```text
Raj created Task A

Ashish updated Project B

John completed Task C

Sarah commented on Task D

Manager approved Sprint E
```

---

## Purpose

Provides visibility into team activity.

Improves collaboration and transparency.

---

# Audit Logs

Activity Feed is for users.

Audit Logs are for administrators.

---

## Activity Feed Example

```text
Task Updated
```

---

## Audit Log Example

```text
User deleted project

Role changed

Permission updated

Workspace archived

Team lead reassigned
```

---

## Purpose

Audit logs provide:

* Accountability
* Security Tracking
* Compliance Support
* Administrative Visibility

---

# Dashboard Widgets

Users can customize their dashboard.

Widgets can be rearranged and configured.

---

## Available Widgets

### Productivity

* My Tasks
* Assigned Tasks
* Completed Tasks

### Knowledge

* Recent Notes
* Favorite Notes

### Analytics

* Productivity Score
* Weekly Progress
* Completion Rate

### Scheduling

* Upcoming Deadlines
* Calendar View

### Communication

* Notifications
* Recent Activity

---

## Future Enhancement

Drag-and-drop dashboard customization.

---

# Calendar View

A dedicated calendar helps users manage deadlines and schedules.

---

## Views

### Daily View

Displays current day's activities.

### Weekly View

Displays work scheduled for the week.

### Monthly View

Displays long-term planning.

---

## Calendar Events

* Tasks
* Deadlines
* Projects
* Meetings
* Reminders

---

# Saved Filters

Users can save commonly used filters.

Examples:

```text
My Open Tasks

Priority High

Due This Week

Assigned By Manager

Completed Today
```

---

# Global Search

The platform provides a unified search experience.

A single search box can search across:

* Notes
* Tasks
* Projects
* Users
* Categories
* Tags

---

## Example Queries

```text
frontend

dashboard

meeting notes

urgent

high priority
```

---

## Benefits

* Faster navigation
* Better knowledge discovery
* Reduced information fragmentation

---

# User Preferences

Every user has personalized settings.

---

## Preferences

### Appearance

* Light Theme
* Dark Theme
* System Theme

---

### Localization

* Language
* Timezone
* Date Format

---

### Notifications

* Email Settings
* Push Settings
* Mention Settings

---

### Dashboard

* Widget Layout
* Default Views
* Saved Filters

---

# Organization Settings

Workspace administrators can configure organization-wide settings.

---

## Organization Configuration

### Branding

* Company Name
* Logo
* Brand Colors

---

### Time Management

* Timezone
* Working Hours

---

### Notifications

* Organization Notification Rules

---

### Security

* Password Policies
* Session Policies
* Authentication Rules

---

# Invitations System

Users join workspaces through invitations.

---

## Workflow

```text
Admin
  ↓
Invite User
  ↓
Email Sent
  ↓
Accept Invitation
  ↓
Join Workspace
```

---

## Features

* Invite by Email
* Accept Invitation
* Reject Invitation
* Expiration Date
* Resend Invitation

---

## Database Table

```text
workspace_invitations
```

---

# Task Assignment History

The platform tracks task ownership changes.

---

## Example

```text
Task Assigned → John

Task Reassigned → Sarah

Task Reassigned → Mike
```

---

## Benefits

* Accountability
* Auditability
* Historical Tracking

---

## Database Table

```text
task_assignment_history
```

---

# Soft Delete & Archive Strategy

The platform avoids permanent deletion whenever possible.

---

## Instead Of

```text
Delete Project
```

Use:

```text
Archive Project
```

---

## Instead Of

```text
Delete Note
```

Use:

```text
Archive Note
```

---

## Instead Of

```text
Delete Task
```

Use:

```text
Archive Task
```

---

## Common Fields

```text
is_archived

archived_at

deleted_at
```

---

# User Presence

The platform can track user activity status.

---

## Status Types

* Online
* Offline
* Away
* Busy

---

## Additional Metadata

```text
last_seen
```

Example:

```text
Last Seen:
5 minutes ago
```

---

# Kanban Board

The platform supports drag-and-drop task management.

Inspired by:

* Trello
* Jira
* ClickUp

---

## Columns

```text
Backlog

Todo

In Progress

Review

Completed
```

---

## Features

* Drag & Drop
* Status Updates
* Real-Time Reordering
* Team Visibility

---

## Technology

```text
@dnd-kit/core

@dnd-kit/sortable

@dnd-kit/utilities
```

---

# Analytics & Reporting

The platform provides productivity insights at multiple levels.

---

## Individual Analytics

* Tasks Completed
* Productivity Trends
* Time-Based Reports
* Completion Rate

---

## Team Analytics

* Team Velocity
* Team Workload
* Team Progress

---

## Workspace Analytics

* Workspace Activity
* Active Members
* Project Performance

---

## Administrative Analytics

* User Growth
* Activity Distribution
* Resource Usage
* Organization Performance

---

## Reports

* Daily Reports
* Weekly Reports
* Monthly Reports
* Custom Date Range Reports

---

# API Standards

The Team Productivity Platform follows an API-First architecture.

All business logic resides in backend services.

Clients consume APIs through a consistent contract.

Supported clients:

* Web Application
* Mobile Application
* Future Desktop Application
* Future Third-Party Integrations

---

## RESTful API Design

All APIs follow REST principles.

Examples:

```http
GET    /tasks
GET    /tasks/:id

POST   /tasks

PATCH  /tasks/:id

DELETE /tasks/:id
```

---

## Response Format

Successful Response

```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {}
}
```

---

Error Response

```json
{
  "success": false,
  "message": "Task not found",
  "errors": []
}
```

---

# Pagination Standards

Every list endpoint must support:

* Pagination
* Search
* Sorting
* Filtering

---

## Example

```http
GET /tasks?page=1
```

---

## Example With Filtering

```http
GET /tasks?page=1&limit=20
```

---

## Example With Search

```http
GET /tasks?page=1&limit=20&search=frontend
```

---

## Full Example

```http
GET /tasks?page=1&limit=20&search=frontend&status=in-progress&sortBy=createdAt
```

---

# Filtering

Supported across most modules.

Examples:

```http
GET /tasks?priority=high

GET /tasks?status=completed

GET /projects?status=active

GET /notes?tag=backend
```

---

# Sorting

Examples:

```http
GET /tasks?sortBy=createdAt

GET /tasks?sortBy=priority

GET /projects?sortBy=deadline
```

---

# Search

Examples:

```http
GET /notes?search=authentication

GET /projects?search=dashboard

GET /tasks?search=frontend
```

---

# Performance Requirements

The platform is designed with performance as a primary objective.

---

# Frontend Performance

## Server Components First

Next.js Server Components are used by default.

Client Components are used only when required.

Benefits:

* Smaller JS Bundles
* Faster Initial Load
* Better SEO
* Improved Performance

---

## Route Splitting

Pages load only required code.

Benefits:

* Faster Navigation
* Smaller Bundles

---

## Lazy Loading

Used for:

* Large Charts
* Rich Text Editors
* Complex Components

---

## Dynamic Imports

Examples:

```typescript
const AnalyticsChart = dynamic(() =>
  import("./analytics-chart")
);
```

---

## React Query Caching

Reduces unnecessary API requests.

Benefits:

* Better UX
* Faster Data Access
* Reduced Backend Load

---

## Debounced Search

Prevents excessive API calls.

Example:

```text
User Types
    ↓
Wait 300ms
    ↓
Execute Search
```

---

## Optimistic Updates

Updates UI immediately before server confirmation.

Examples:

* Task Status Changes
* Note Updates
* Favorites

---

## Image Optimization

Next.js image optimization will be used for:

* Profile Pictures
* Project Images
* Attachments

---

# Backend Performance

## Pagination Everywhere

No endpoint should return large datasets without pagination.

---

## Prevent N+1 Queries

Load only required relationships.

Bad:

```text
100 tasks
100 users
100 additional queries
```

Good:

```text
Single optimized query
```

---

## Database Indexing

Indexes should exist on:

```text
email

user_id

workspace_id

project_id

status

created_at

updated_at
```

---

## Load Required Relations Only

Example:

Bad:

```typescript
relations: ["user", "workspace", "team", "tasks"]
```

Good:

```typescript
relations: ["user"]
```

---

# System Architecture

The platform follows a service-oriented architecture.

```text
                 ┌─────────────────┐
                 │     Web App     │
                 │    Next.js      │
                 └────────┬────────┘
                          │
                          │
                 ┌────────▼────────┐
                 │   API Layer     │
                 └────────┬────────┘
                          │
       ┌──────────────────┼──────────────────┐
       │                                     │
       │                                     │
┌──────▼──────┐                    ┌────────▼───────┐
│   FastAPI   │                    │    NestJS      │
│ Microservice│                    │ Microservice   │
└──────┬──────┘                    └────────┬───────┘
       │                                     │
       └──────────────────┬──────────────────┘
                          │
                   ┌──────▼──────┐
                   │ PostgreSQL  │
                   └─────────────┘
```

---

# Service Responsibilities

Each service owns a specific business domain.

---

# FastAPI Responsibilities

FastAPI acts as the Identity and Knowledge Service.

---

## Authentication

* Registration
* Login
* Logout
* Refresh Tokens
* Password Reset
* Email Verification

---

## User Management

* User Profiles
* User Preferences
* User Settings

---

## Notes Management

* Create Notes
* Update Notes
* Archive Notes
* Search Notes

---

## Books Integration

* Open Library API
* Knowledge Resources

---

# NestJS Responsibilities

NestJS acts as the Productivity Service.

---

## Tasks

* Create Tasks
* Assign Tasks
* Track Progress

---

## Categories

* Organize Tasks
* Organize Notes

---

## Tags

* Searchability
* Classification

---

## Notifications

* User Notifications
* Team Notifications

---

## Analytics

* Productivity Reports
* Team Metrics

---

## Activity Logs

* User Activities
* Audit Events

---

## Future Modules

* Projects
* Teams
* Workspaces
* Permissions
* Invitations
* Comments
* Attachments

---

# API Ownership Matrix

| Feature        | FastAPI | NestJS |
| -------------- | ------- | ------ |
| Authentication | ✅       | ❌      |
| Users          | ✅       | ❌      |
| Notes          | ✅       | ❌      |
| Books          | ✅       | ❌      |
| Tasks          | ❌       | ✅      |
| Categories     | ❌       | ✅      |
| Tags           | ❌       | ✅      |
| Notifications  | ❌       | ✅      |
| Analytics      | ❌       | ✅      |
| Activity Logs  | ❌       | ✅      |
| Projects       | ❌       | ✅      |
| Teams          | ❌       | ✅      |
| Workspaces     | ❌       | ✅      |

---

# Authentication Flow

```text
User
  │
  ▼
Login Request
  │
  ▼
FastAPI
  │
  ▼
Validate Credentials
  │
  ▼
Generate JWT
  │
  ▼
Return Access Token
  │
  ▼
Frontend Stores Token
  │
  ▼
Future Requests
```

---

# Cross-Service Authorization

NestJS trusts JWT tokens generated by FastAPI.

Flow:

```text
Login
   │
   ▼
FastAPI
   │
   ▼
JWT Issued
   │
   ▼
Frontend
   │
   ▼
NestJS Request
   │
   ▼
JWT Validation
   │
   ▼
Authorized
```

---

# Request Lifecycle

Example: Create Task

```text
Frontend
   │
   ▼
Tasks Page
   │
   ▼
React Query
   │
   ▼
Axios Client
   │
   ▼
NestJS Controller
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
PostgreSQL
   │
   ▼
Response
```

---

# Web Application Architecture

Technology Stack:

```text
Next.js 16
React 19
TypeScript
Tailwind CSS
Shadcn UI
React Query
Axios
Zustand
```

Architecture:

```text
Pages
  │
Components
  │
Feature Hooks
  │
Services
  │
API Clients
  │
Backend APIs
```

---

# Mobile Application Architecture

Technology Stack:

```text
Flutter
Dart
Riverpod
Dio
GoRouter
```

Architecture:

```text
Screens
  │
Providers
  │
Repositories
  │
Services
  │
API Clients
  │
Backend APIs
```

---

# Database Architecture

Primary Database:

```text
PostgreSQL
```

Used By:

* FastAPI
* NestJS

---

# Core Entities

```text
users

notes

tasks

categories

tags

task_tags

projects

teams

workspaces

notifications

activity_logs

comments

attachments

favorites

workspace_invitations

task_assignment_history
```

---

# Deployment Architecture

```text
                    Internet
                        │
                        ▼
                  Nginx Gateway
                        │
       ┌────────────────┼────────────────┐
       │                                 │
       ▼                                 ▼
   Next.js                         Flutter App
       │
       ▼
 ┌─────────────┬─────────────┐
 ▼                           ▼
FastAPI                  NestJS
 │                           │
 └─────────────┬─────────────┘
               ▼
          PostgreSQL
```

---

# Docker Architecture

All services run through Docker Compose.

```text
docker-compose
│
├── postgres
│
├── fastapi-backend
│
├── nestjs-backend
│
└── web
```

Future:

```text
redis

nginx

minio

rabbitmq
```

---

# Scalability Strategy

The platform is designed for future expansion.

Future capabilities include:

* Multi-Tenant Organizations
* Workspace Isolation
* Real-Time Collaboration
* WebSockets
* Background Jobs
* Event-Driven Architecture
* Desktop Applications
* Public API Integrations
* AI-Powered Productivity Features

---

# Design Principles

The platform follows these principles:

1. Performance First
2. API First
3. Security First
4. Scalability First
5. Developer Experience
6. Modular Architecture
7. Clean Code
8. Testability
9. Maintainability
10. Extensibility

These principles guide every architectural and implementation decision throughout the platform.

---

# Database Schema

The platform uses PostgreSQL as the primary database.

The schema is designed around:

* Multi-Workspace Support
* Team Collaboration
* Task Management
* Knowledge Management
* Analytics
* Activity Tracking
* Future Scalability

---

# Core Tables

## Users

Stores platform users.

```sql
users
```

Fields:

```text
id

email

username

first_name

last_name

password_hash

avatar_url

role

is_active

email_verified

last_login

created_at

updated_at
```

---

## Refresh Tokens

Stores active refresh tokens.

```sql
refresh_tokens
```

Fields:

```text
id

user_id

token

expires_at

revoked_at

created_at
```

---

## Notes

Stores user notes and knowledge documents.

```sql
notes
```

Fields:

```text
id

user_id

title

content

is_archived

archived_at

deleted_at

created_at

updated_at
```

---

## Categories

```sql
categories
```

Fields:

```text
id

name

slug

description

created_at

updated_at
```

---

## Tags

```sql
tags
```

Fields:

```text
id

name

slug

created_at

updated_at
```

---

## Tasks

```sql
tasks
```

Fields:

```text
id

title

description

status

priority

start_date

due_date

reminder_date

assigned_to

created_by

category_id

parent_task_id

is_recurring

repeat_type

next_due_date

is_archived

archived_at

deleted_at

created_at

updated_at
```

---

## Task Tags

Many-to-many relationship.

```sql
task_tags
```

Fields:

```text
task_id

tag_id
```

---

## Projects

```sql
projects
```

Fields:

```text
id

workspace_id

name

description

status

progress

start_date

due_date

created_by

is_archived

created_at

updated_at
```

---

## Project Members

```sql
project_members
```

Fields:

```text
project_id

user_id

role
```

---

## Workspaces

```sql
workspaces
```

Fields:

```text
id

name

slug

description

logo_url

timezone

created_by

created_at

updated_at
```

---

## Workspace Members

```sql
workspace_members
```

Fields:

```text
workspace_id

user_id

role

joined_at
```

---

## Teams

```sql
teams
```

Fields:

```text
id

workspace_id

name

description

lead_id

created_at

updated_at
```

---

## Team Members

```sql
team_members
```

Fields:

```text
team_id

user_id

joined_at
```

---

## Comments

```sql
comments
```

Fields:

```text
id

user_id

task_id

project_id

note_id

parent_comment_id

content

created_at

updated_at
```

---

## Comment Mentions

```sql
comment_mentions
```

Fields:

```text
comment_id

mentioned_user_id
```

---

## Attachments

```sql
attachments
```

Fields:

```text
id

user_id

task_id

project_id

note_id

comment_id

file_name

file_url

file_size

mime_type

created_at
```

---

## Notifications

```sql
notifications
```

Fields:

```text
id

user_id

type

title

message

is_read

created_at
```

---

## Activity Logs

```sql
activity_logs
```

Fields:

```text
id

user_id

action

entity_type

entity_id

metadata

created_at
```

---

## Favorites

```sql
favorites
```

Fields:

```text
id

user_id

entity_type

entity_id

created_at
```

---

## Workspace Invitations

```sql
workspace_invitations
```

Fields:

```text
id

workspace_id

email

invited_by

status

expires_at

created_at
```

---

## Task Assignment History

```sql
task_assignment_history
```

Fields:

```text
id

task_id

assigned_from

assigned_to

assigned_at
```

---

# Entity Relationship Overview

```text
Workspace
│
├── Teams
│   └── Team Members
│
├── Projects
│   └── Project Members
│
└── Users
     │
     ├── Notes
     ├── Tasks
     ├── Comments
     ├── Notifications
     └── Activity Logs
```

---

# FastAPI Folder Structure

```text
apps/
└── fastapi-backend/
    │
    ├── alembic/
    │
    ├── app/
    │
    ├── api/
    │   ├── routes/
    │   │   ├── auth.py
    │   │   ├── users.py
    │   │   ├── notes.py
    │   │   ├── books.py
    │   │   └── health.py
    │   │
    │   └── deps.py
    │
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   ├── logging.py
    │   └── constants.py
    │
    ├── db/
    │   ├── base.py
    │   └── session.py
    │
    ├── models/
    │
    ├── schemas/
    │
    ├── services/
    │
    ├── repositories/
    │
    ├── middleware/
    │
    ├── integrations/
    │
    ├── utils/
    │
    └── main.py
```

---

# NestJS Folder Structure

```text
apps/
└── nestjs-backend/
    │
    ├── src/
    │
    ├── config/
    │
    ├── common/
    │
    ├── database/
    │
    ├── integrations/
    │
    ├── modules/
    │   │
    │   ├── auth/
    │   ├── tasks/
    │   ├── categories/
    │   ├── tags/
    │   ├── notifications/
    │   ├── analytics/
    │   ├── activity-logs/
    │   │
    │   ├── projects/
    │   ├── teams/
    │   ├── workspaces/
    │   ├── permissions/
    │   ├── invitations/
    │   ├── comments/
    │   └── attachments/
    │
    └── main.ts
```

---

# Next.js Folder Structure

```text
apps/
└── web/
    │
    ├── public/
    │
    ├── src/
    │   │
    │   ├── app/
    │   ├── components/
    │   ├── features/
    │   ├── services/
    │   ├── store/
    │   ├── providers/
    │   ├── hooks/
    │   ├── lib/
    │   ├── types/
    │   ├── constants/
    │   └── utils/
    │
    └── package.json
```

---

# Flutter Folder Structure

```text
apps/
└── mobile/
    │
    ├── lib/
    │
    ├── features/
    │
    ├── services/
    │
    ├── providers/
    │
    ├── models/
    │
    ├── routes/
    │
    ├── widgets/
    │
    └── main.dart
```

---

# Environment Variables

## FastAPI

```env
DATABASE_URL=

JWT_SECRET_KEY=

JWT_ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

REFRESH_TOKEN_EXPIRE_DAYS=

REDIS_URL=
```

---

## NestJS

```env
PORT=

DATABASE_HOST=

DATABASE_PORT=

DATABASE_NAME=

DATABASE_USER=

DATABASE_PASSWORD=

JWT_SECRET=

JWT_ISSUER=

JWT_AUDIENCE=
```

---

## Web

```env
NEXT_PUBLIC_FASTAPI_URL=

NEXT_PUBLIC_NESTJS_URL=

NEXT_PUBLIC_APP_NAME=
```

---

## Mobile

```env
FASTAPI_BASE_URL=

NESTJS_BASE_URL=
```

---

# Local Development Setup

## Clone Repository

```bash
git clone <repository-url>

cd team-productivity-platform
```

---

## Start FastAPI

```bash
cd apps/fastapi-backend

uvicorn app.main:app --reload
```

---

## Start NestJS

```bash
cd apps/nestjs-backend

npm install

npm run start:dev
```

---

## Start Web

```bash
cd apps/web

npm install

npm run dev
```

---

## Start Mobile

```bash
cd apps/mobile

flutter pub get

flutter run
```

---

# Docker Setup

Run all services:

```bash
docker compose up --build
```

---

Services:

```text
postgres

fastapi-backend

nestjs-backend

web
```

---

# Testing Strategy

## FastAPI

```text
pytest

pytest-asyncio

pytest-cov
```

Coverage:

* Services
* Routes
* Authentication
* Database

---

## NestJS

```text
Jest

Supertest
```

Coverage:

* Services
* Controllers
* Guards
* DTO Validation

---

## Frontend

```text
React Testing Library

Vitest (Future)
```

---

## E2E

Future:

```text
Playwright
```

---

# CI/CD Pipeline

Future GitHub Actions Pipeline:

```text
Push
 │
 ▼
Lint
 │
 ▼
Unit Tests
 │
 ▼
Build
 │
 ▼
Docker Build
 │
 ▼
Deploy
```

---

# Future Roadmap

## Phase 1

* Authentication
* Notes
* Tasks
* Categories
* Tags

---

## Phase 2

* Notifications
* Analytics
* Activity Logs

---

## Phase 3

* Projects
* Teams
* Workspaces

---

## Phase 4

* Comments
* Attachments
* Invitations

---

## Phase 5

* Calendar
* Global Search
* Dashboard Widgets

---

## Phase 6

* Real-Time Collaboration
* WebSockets
* Presence Tracking

---

## Phase 7

* AI Productivity Assistant
* AI Note Summaries
* AI Task Suggestions

---

# Contributing

Development Guidelines:

1. Follow Clean Architecture
2. Follow SOLID Principles
3. Write Tests
4. Use TypeScript Strict Mode
5. Follow API Standards
6. Use Feature-Based Frontend Architecture
7. Prefer Reusable Components

---

# License

This project is licensed under the MIT License.

---

# Final Summary

The Team Productivity Platform is a modern productivity ecosystem built to unify:

* Notes
* Tasks
* Projects
* Teams
* Workspaces
* Knowledge Management
* Collaboration
* Analytics
* Notifications

into a single scalable platform.

Inspired by:

* Notion
* Todoist
* Trello
* Jira

while maintaining:

* Performance First
* API First
* Security First
* Scalability First

through FastAPI, NestJS, Next.js, Flutter, PostgreSQL, and Docker-based infrastructure.
