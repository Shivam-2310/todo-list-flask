# Flask Todo List Application

A secure web-based task management application built with Flask, featuring user authentication, CRUD operations, and comprehensive input validation.

## Features

### Core Functionality
- **User Registration & Authentication**: Secure user account creation and login system
- **Personal Task Management**: Create, read, update, and delete tasks with user isolation
- **Task Status Tracking**: Mark tasks as complete/incomplete with timestamp tracking
- **Search & Filter**: Find tasks quickly with search functionality
- **Dashboard Statistics**: View total, completed, and pending task counts
- **Responsive UI**: Professional dark-themed interface using Bootstrap 5

### Security Features
- **Session-based Authentication**: Secure user sessions with login protection
- **Password Security**: Werkzeug password hashing with salt
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Input Sanitization**: Server-side validation and XSS prevention
- **User Data Isolation**: Users can only access their own tasks

## Validation & Security Measures

### User Registration Validations
- **Username Validation**:
  - 3-20 characters length requirement
  - Alphanumeric characters and underscores only
  - Unique username constraint
  - Required field validation

- **Password Validation**:
  - Minimum 8 characters required
  - Must contain uppercase letter
  - Must contain lowercase letter  
  - Must contain at least one digit
  - Password confirmation match verification

### Task Management Validations
- **Title Validation**:
  - Required field (cannot be empty)
  - Maximum 200 characters limit
  - Minimum 3 characters requirement
  - Whitespace trimming

- **Description Validation**:
  - Optional field
  - Maximum 200 characters limit
  - Whitespace trimming

### Security Validations
- **Authentication Checks**:
  - Login required for all task operations
  - User ownership verification for all CRUD operations
  - Session validation on protected routes

- **HTTP Security**:
  - POST method enforcement for data modifications
  - CSRF token validation on all forms
  - Secure delete/toggle operations (no GET requests)

- **Database Security**:
  - SQLAlchemy ORM prevents SQL injection
  - Parameterized queries for all database operations
  - Automatic transaction rollback on errors

### Frontend Validations
- **Real-time Validation**:
  - Live character counters for title/description
  - Color-coded feedback (warning at 150+ chars, danger at 180+)
  - Form submission prevention for invalid data
  - Dynamic input validation styling

- **User Experience**:
  - Confirmation dialogs for destructive actions
  - Loading states for form submissions
  - Auto-focus on form fields
  - Keyboard shortcuts (Ctrl+S to save)

## Technical Stack

- **Backend**: Flask, SQLAlchemy, Flask-WTF
- **Database**: SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Security**: Werkzeug, CSRF Protection

## Installation & Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access at: `http://localhost:5000`

## Database Schema

### Users Table
- Primary key, unique username, hashed password, creation timestamp

### Tasks Table  
- Primary key, title, description, completion status, timestamps, user foreign key

---

**Flask Todo Application** - Secure task management with comprehensive validation.