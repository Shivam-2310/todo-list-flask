from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
import os
import re

# IST TIMEZONE CONFIGURATION FOR INDIAN USERS
IST = timezone(timedelta(hours=5, minutes=30))

def convert_utc_to_ist(utc_datetime):
    """Convert UTC datetime to IST for display"""
    if utc_datetime is None:
        return None
    
    # HANDLE NAIVE DATETIME OBJECTS BY ASSUMING UTC
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    
    ist_datetime = utc_datetime.astimezone(IST)
    return ist_datetime

app = Flask(__name__)

# FLASK APPLICATION CONFIGURATION
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INITIALIZE SECURITY AND DATABASE COMPONENTS
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# JINJA2 TEMPLATE FILTER FOR TIMEZONE CONVERSION
@app.template_filter('ist')
def ist_filter(utc_datetime):
    """Template filter to convert UTC to IST"""
    return convert_utc_to_ist(utc_datetime)
# DATABASE MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ONE-TO-MANY RELATIONSHIP: USER CAN HAVE MULTIPLE TASKS
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Task {self.title}>'

# VALIDATION UTILITIES
def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_username(username):
    """Validate username"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 20:
        return False, "Username must be less than 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Username is valid"

# AUTHENTICATION DECORATOR FOR PROTECTED ROUTES
def login_required(f):
    """Decorator to require login for certain routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# APPLICATION ROUTES
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise show welcome"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # INPUT VALIDATION PIPELINE
        if not username:
            flash('Username is required.', 'error')
            return render_template('register.html')
        
        if not password:
            flash('Password is required.', 'error')
            return render_template('register.html')
        
        username_valid, username_msg = validate_username(username)
        if not username_valid:
            flash(username_msg, 'error')
            return render_template('register.html')
        
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            flash(password_msg, 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # ENSURE USERNAME UNIQUENESS
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html')
        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        # AUTHENTICATE USER WITH DATABASE LOOKUP
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - show user's tasks"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found. Please log in again.', 'error')
        return redirect(url_for('login'))
    
    # TASK FILTERING AND SEARCH FUNCTIONALITY
    search_query = request.args.get('search', '').strip()
    tasks_query = Task.query.filter_by(user_id=user.id)
    
    if search_query:
        tasks_query = tasks_query.filter(Task.title.contains(search_query))
    
    tasks = tasks_query.order_by(Task.created_at.desc()).all()
    
    # DASHBOARD STATISTICS CALCULATION
    total_tasks = len(tasks) if search_query else Task.query.filter_by(user_id=user.id).count()
    completed_tasks = len([t for t in tasks if t.completed])
    incomplete_tasks = total_tasks - completed_tasks
    
    return render_template('dashboard.html', 
                         user=user, 
                         tasks=tasks, 
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         incomplete_tasks=incomplete_tasks,
                         search_query=search_query,
                         convert_utc_to_ist=convert_utc_to_ist)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    """Add a new task"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    # TASK INPUT VALIDATION
    if not title:
        flash('Task title is required.', 'error')
        return redirect(url_for('dashboard'))
    
    if len(title) > 200:
        flash('Task title must be less than 200 characters.', 'error')
        return redirect(url_for('dashboard'))
    
    if len(description) > 200:
        flash('Task description must be less than 200 characters.', 'error')
        return redirect(url_for('dashboard'))
    try:
        task = Task(
            title=title,
            description=description,
            user_id=session['user_id']
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the task. Please try again.', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = Task.query.get_or_404(task_id)
    
    # AUTHORIZATION: ENSURE USER OWNS THE TASK
    if task.user_id != session['user_id']:
        flash('You can only edit your own tasks.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        # VALIDATE EDITED TASK DATA
        if not title:
            flash('Task title is required.', 'error')
            return render_template('edit_task.html', task=task, convert_utc_to_ist=convert_utc_to_ist)
        
        if len(title) > 200:
            flash('Task title must be less than 200 characters.', 'error')
            return render_template('edit_task.html', task=task, convert_utc_to_ist=convert_utc_to_ist)
        
        if len(description) > 200:
            flash('Task description must be less than 200 characters.', 'error')
            return render_template('edit_task.html', task=task, convert_utc_to_ist=convert_utc_to_ist)
        try:
            task.title = title
            task.description = description
            task.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the task. Please try again.', 'error')
    
    return render_template('edit_task.html', task=task, convert_utc_to_ist=convert_utc_to_ist)

@app.route('/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    """Toggle task completion status"""
    task = Task.query.get_or_404(task_id)
    
    # AUTHORIZATION CHECK FOR TASK OWNERSHIP
    if task.user_id != session['user_id']:
        flash('You can only modify your own tasks.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        status = "completed" if task.completed else "marked as incomplete"
        flash(f'Task "{task.title}" {status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the task. Please try again.', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # AUTHORIZATION CHECK FOR TASK DELETION
    if task.user_id != session['user_id']:
        flash('You can only delete your own tasks.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f'Task "{task.title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the task. Please try again.', 'error')
    
    return redirect(url_for('dashboard'))

# HTTP ERROR HANDLERS
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# DATABASE INITIALIZATION
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    # APPLICATION STARTUP SEQUENCE
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
