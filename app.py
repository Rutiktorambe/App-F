from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'  # Required for session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect users to login page if not logged in

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('ems_user.db')  # Ensure the correct path to your SQLite database
    conn.row_factory = sqlite3.Row  # This allows us to return rows as dictionaries
    return conn

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, fname, lname, role, team):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.role = role
        self.team = team

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM EMS_users WHERE EmployeeID = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['EmployeeID'], user['Fname'], user['Lname'], user['Role'], user['Team'])
    return None

# Route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ems_login = request.form['ems_login']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM EMS_users WHERE EMSlogin = ? AND Password = ?', (ems_login, password)).fetchone()
        conn.close()
        
        if user:
            user_obj = User(user['EmployeeID'], user['Fname'], user['Lname'], user['Role'], user['Team'])
            login_user(user_obj)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
    
    return render_template('login.html')

# Route for home page (protected)
@app.route('/home')
@login_required
def home():
    return render_template('home.html', fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team)

# Route for Timesheet Home Page
@app.route('/timesheet_home')
@login_required
def timesheet_home():
    conn = get_db_connection()
    
    # Check if the logged-in user is a manager
    manager_of_anyone = conn.execute('SELECT 1 FROM EMS_users WHERE ManagerID = ?', (current_user.id,)).fetchone()
    conn.close()
    
    # Render the timesheet home page with a flag for whether the user is a manager
    return render_template('timesheet_home.html', is_manager=bool(manager_of_anyone))

# Route for Fill Timesheet (example)
@app.route('/fill_timesheet', methods=['GET', 'POST'])
@login_required
def fill_timesheet():
    if request.method == 'POST':
        # Fetch form data
        duration_hours = int(request.form['duration_hours'])
        duration_minutes = int(request.form['duration_minutes'])
        project_code = request.form['project_code']
        allocation_type = request.form['allocation_type']
        holiday_status = request.form['holiday_status']
        category_1 = request.form['category_1']
        category_2 = request.form['category_2']
        category_3 = request.form['category_3']
        comments = request.form['comments']
        
        # Calculate total time in hours
        total_time = duration_hours + (duration_minutes / 60.0)
        
        # Set unavailable_time based on holiday status
        if holiday_status == 'Full Day':
            unavailable_time = 7
        elif holiday_status == 'Half Day':
            unavailable_time = 3
        else:
            unavailable_time = 0
        
        # Insert into timesheet_entries table
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO timesheet_entries 
            (employee_id, fname, lname, team, manager_name, duration_hours, duration_minutes, total_time, 
            project_code, allocation_type, holiday_status, unavailable_time, category_1, category_2, category_3, comments) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (current_user.id, current_user.fname, current_user.lname, current_user.team, current_user.manager_name,
            duration_hours, duration_minutes, total_time, project_code, allocation_type, holiday_status, 
            unavailable_time, category_1, category_2, category_3, comments)
        )
        conn.commit()
        conn.close()
        
        flash('Timesheet entry submitted successfully!', 'success')
        return redirect(url_for('timesheet_home'))

    # Render form
    return render_template('fill_timesheet.html')


# Route for View Summary (example)
@app.route('/view_summary')
@login_required
def view_summary():
    return "View Summary Page"

# Route for Manage Repotree (example)
@app.route('/manage_repotree')
@login_required
def manage_repotree():
    # Make sure that only managers can access this page
    conn = get_db_connection()
    manager_of_anyone = conn.execute('SELECT 1 FROM EMS_users WHERE ManagerID = ?', (current_user.id,)).fetchone()
    conn.close()
    
    if not manager_of_anyone:
        return "Unauthorized", 403
    
    return "Manage Repotree Page"

# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Custom error handler for unauthorized access
@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to log in first!', 'error')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
