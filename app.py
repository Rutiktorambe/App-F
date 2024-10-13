from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from datetime import datetime
from datetime import datetime, timedelta



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
    def __init__(self, id, fname, lname, role, team, managername):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.role = role
        self.team = team
        self.managername =managername

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM EMS_users WHERE EmployeeID = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['EmployeeID'], user['Fname'], user['Lname'], user['Role'], user['Team'] ,user['ManagerName'])
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
            user_obj = User(user['EmployeeID'], user['Fname'], user['Lname'], user['Role'], user['Team'],user['ManagerName'])
            login_user(user_obj)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
    
    return render_template('login.html')

# Route for home page (protected)
@app.route('/home')
@login_required
def home():
    return render_template('home.html', fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)

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

# Fill timesheet route
@app.route('/fill_timesheet', methods=['GET', 'POST'])
@login_required
def fill_timesheet():
    if request.method == 'POST':
        # Process the form submission
        employee_id = request.form['employee_id']
        fname = request.form['fname']
        lname = request.form['lname']
        team = request.form['team']
        manager_name = request.form['manager_name']
        selected_dates = request.form['dates'].split(",")  # Get all selected dates
        duration_hours = int(request.form['duration_hours'])
        duration_minutes = int(request.form['duration_minutes'])
        total_time = round(duration_hours + (duration_minutes / 60), 2)
        allocation_type = request.form['allocation_type']
        category_1 = request.form.get('category_1')  
        category_2 = request.form.get('category_2')
        category_3 = request.form.get('category_3')
        comments = request.form['comments']

        # Insert data for each selected date
        try:
            conn = get_db_connection()
            for date in selected_dates:
                conn.execute('''INSERT INTO timesheet_entries (employee_id, fname, lname, team, manager_name, date, duration_hours, duration_minutes, total_time, allocation_type, category_1, category_2, category_3, comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (employee_id, fname, lname, team, manager_name, date, duration_hours, duration_minutes, total_time, allocation_type, category_1, category_2, category_3, comments))
            conn.commit()
            conn.close()
            flash('Timesheet submitted successfully!', 'success')
            return redirect(url_for('success'))  # Redirect to a success page
        except Exception as e:
            flash(f"Error occurred while submitting timesheet: {str(e)}", 'error')

    # Render the form initially
    return render_template('fill_timesheet.html')




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

@app.route('/success')
@login_required
def success():
    return render_template('success.html')  # Create a success.html template


@app.route('/view_summary', methods=['GET'])
@login_required
def view_summary():
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    current_date = datetime.strptime(selected_date, '%Y-%m-%d')

    start_date = current_date - timedelta(days=current_date.weekday())
    end_date = start_date + timedelta(days=6)

    summary = {
        "dates": {f"{(start_date + timedelta(days=i)).strftime('%Y-%m-%d')}": {} for i in range(7)},
        "totals": {
            "admin": 0,
            "billable": 0,
            "non-billable": 0,
            "total_time": 0
        }
    }

    try:
        conn = get_db_connection()
        entries = conn.execute(
            'SELECT * FROM timesheet_entries WHERE date BETWEEN ? AND ? AND employee_id = ?',
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), current_user.id)
        ).fetchall()
        conn.close()

        print("Entries fetched:", entries)  # Debugging line

        # Process each entry
        for entry in entries:
            date = entry['date']
            allocation_type = entry['allocation_type']
            total_time = entry['total_time']

            if allocation_type in ['admin', 'billable', 'non-billable']:
                summary['dates'][date].setdefault(allocation_type, 0)
                summary['dates'][date][allocation_type] += total_time
                summary['totals'][allocation_type] += total_time

            summary['dates'][date].setdefault('total_time', 0)
            summary['dates'][date]['total_time'] += total_time
            summary['totals']['total_time'] += total_time

    except Exception as e:
        print("An error occurred:", str(e))
        flash("An error occurred while generating the summary.", 'error')
        return redirect(url_for('home'))

    return render_template('view_summary.html', summary=summary, start_date=start_date.strftime('%Y-%m-%d'))



@app.route('/view_summary/next_week', methods=['GET'])
@login_required
def next_week():
    # Redirect to the view_summary route with the date for the next week
    current_date = request.args.get('start_date')
    next_date = datetime.strptime(current_date, '%Y-%m-%d') + timedelta(weeks=1)
    return redirect(url_for('view_summary', date=next_date.strftime('%Y-%m-%d')))

@app.route('/view_summary/previous_week', methods=['GET'])
@login_required
def previous_week():
    # Redirect to the view_summary route with the date for the previous week
    current_date = request.args.get('start_date')
    previous_date = datetime.strptime(current_date, '%Y-%m-%d') - timedelta(weeks=1)
    return redirect(url_for('view_summary', date=previous_date.strftime('%Y-%m-%d')))




@app.route('/edit_entry/<int:entry_id>', methods=['POST'])
@login_required
def edit_entry(entry_id):
    # Handle editing logic here
    # Update the database with the new entry details
    # Return success message
    pass

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM timesheet_entries WHERE entree_id = ?', (entry_id,))
        conn.commit()
        conn.close()
        flash('Entry deleted successfully', 'success')
    except Exception as e:
        flash(f'Error occurred while deleting entry: {str(e)}', 'error')
    return redirect(url_for('weekly_summary'))













if __name__ == "__main__":
    app.run(debug=True)
