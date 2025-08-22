# Todo List - Flask Web Application Project

A Flask web application for personal task management with user authentication and a clean, dark UI interface.

## Features

### 🔐 **Secure Authentication**
- User registration with strong password validation
- Secure password hashing using Werkzeug
- Session-based authentication
- Per-user task isolation

### 📝 **Task Management**
- Create, read, update, and delete tasks
- Task completion tracking
- Search and filter functionality
- Task statistics and progress tracking

### 🎨 **Professional UI**
- Modern Bootstrap 5 design
- Responsive layout for all devices
- Professional color scheme and animations
- Intuitive user experience

### 🛡️ **Security & Validation**
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Strong password requirements

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project:**
   ```bash
   git clone <your-repo-url>
   cd flask-todo-list
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## Usage

### Getting Started
1. **Register a new account** with a unique username and strong password
2. **Log in** to access your personal dashboard
3. **Add your first task** using the form on the left side
4. **Manage your tasks** using the action buttons (complete, edit, delete)

### Features Guide

#### Dashboard
- View task statistics (total, completed, remaining)
- Add new tasks with title and optional description
- Search tasks by title
- Toggle between showing all tasks or just incomplete ones
- Mark tasks as complete/incomplete
- Edit or delete existing tasks

#### Task Management
- **Add Task**: Enter a title (required) and optional description
- **Edit Task**: Modify task details and view creation/update timestamps
- **Complete Task**: Mark tasks as done (they'll be visually distinguished)
- **Delete Task**: Remove tasks with confirmation dialog

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

### Username Requirements
- 3-20 characters
- Letters, numbers, and underscores only
- Must be unique

## Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Security**: Werkzeug password hashing, Flask sessions

### Project Structure
```
flask-todo-list/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── todo_app.db           # SQLite database (created automatically)
└── templates/            # HTML templates
    ├── base.html         # Base template with common layout
    ├── index.html        # Welcome page
    ├── register.html     # User registration
    ├── login.html        # User login
    ├── dashboard.html    # Main task management interface
    ├── edit_task.html    # Task editing form
    ├── 404.html         # Page not found error
    └── 500.html         # Server error page
```

### Database Schema

#### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

#### Tasks Table
- `id`: Primary key
- `title`: Task title (required)
- `description`: Optional task description
- `completed`: Boolean completion status
- `created_at`: Task creation timestamp
- `updated_at`: Last modification timestamp
- `user_id`: Foreign key to users table

## Development

### Running in Development Mode
The application runs in debug mode by default, which provides:
- Automatic code reloading
- Detailed error messages
- Interactive debugger

### Database Management
- Database is automatically created on first run
- Located at `todo_app.db` in the project root
- Uses SQLAlchemy ORM for database operations

### Customization
- Modify CSS variables in `base.html` to change colors
- Update Flask configuration in `app.py`
- Extend models in `app.py` for additional features

## Security Considerations

### For Production Deployment
1. **Change the secret key** in `app.py`
2. **Use environment variables** for sensitive configuration
3. **Enable HTTPS** for secure communication
4. **Use a production database** (PostgreSQL, MySQL)
5. **Implement rate limiting** for API endpoints
6. **Add logging** for security monitoring

### Built-in Security Features
- Password hashing with salt
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention via SQLAlchemy ORM
- XSS protection through template escaping

## Troubleshooting

### Common Issues

**Database errors:**
- Delete `todo_app.db` and restart the application to reset the database

**Port already in use:**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

**Module not found:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Permission errors:**
- Check file permissions in the project directory

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For questions, issues, or contributions, please open an issue in the project repository.

---

**Todo Pro** - Professional task management made simple. ✅
