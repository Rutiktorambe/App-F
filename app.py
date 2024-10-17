from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from datetime import datetime
from datetime import datetime, timedelta



app = Flask(__name__)
app.secret_key = 'secretkey' 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('ems_user.db')  
    conn.row_factory = sqlite3.Row  
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
    return render_template('home.html', id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)

# Route for Timesheet Home Page
@app.route('/timesheet_home')
@login_required
def timesheet_home():
    conn = get_db_connection()
    
    # Check if the logged-in user is a manager
    manager_of_anyone = conn.execute('SELECT 1 FROM EMS_users WHERE ManagerID = ?', (current_user.id,)).fetchone()
    conn.close()
    
    # Render the timesheet home page with a flag for whether the user is a manager
    return render_template('timesheet_home.html', fname=current_user.fname,  lname=current_user.lname,is_manager=bool(manager_of_anyone),id =current_user.id, role=current_user.role, team=current_user.team ,managername=current_user.managername)

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
        selected_dates = request.form['dates'].split(",")  
        duration_hours = int(request.form['duration_hours'])
        duration_minutes = int(request.form['duration_minutes'])
        total_time = round(duration_hours + (duration_minutes / 60), 2)
        allocation_type = request.form['allocation_type']
        category_1 = request.form.get('category_1')  
        category_2 = request.form.get('category_2')
        category_3 = request.form.get('category_3')
        comments = request.form['comments']

        # Initialize time tracking variables
        billable_time = 0
        nonbillable_admin_time = 0
        nonbillable_training_time = 0
        unavailable_time = 0
        holiday_status = None

        # Set the appropriate time based on allocation type
        if allocation_type == 'billable':
            billable_time = total_time
        elif allocation_type == 'non-billable':
            if category_1 == 'admin':
                nonbillable_admin_time = total_time
            elif category_1 == 'training':
                nonbillable_training_time = total_time

        try:
            # Use a context manager for database connection
            with get_db_connection() as conn:
                for date in selected_dates:
                    conn.execute('''
                        INSERT INTO timesheet_entries (
                            employee_id, fname, lname, team, manager_name, date, duration_hours,
                            duration_minutes, billable_time, nonbillable_admin_time, nonbillable_training_time,
                            unavailable_time, total_time, allocation_type, category_1, category_2, category_3, comments
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        employee_id, fname, lname, team, manager_name, date, duration_hours, duration_minutes,
                        billable_time, nonbillable_admin_time, nonbillable_training_time, unavailable_time,
                        total_time, allocation_type, category_1, category_2, category_3, comments
                    ))
                conn.commit()
            return redirect(url_for('success'))  # Redirect to a success page
        except Exception as e:
            flash(f"Error occurred while submitting timesheet: {str(e)}", 'error')

    # Render the form initially
    return render_template('fill_timesheet.html', id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)



@app.route('/view_repotree', methods=['GET', 'POST'])
@login_required
def view_repotree():
    edit_entry = None
    edit_entry_id = request.args.get('edit_entry_id')

    if request.method == 'POST':
        entry_id = request.form.get('entry_id')
        project_code = request.form.get('project_code')

        # Update the project code in the database
        conn = get_db_connection()
        conn.execute(
            'UPDATE timesheet_entries SET project_code = ? WHERE entree_id = ?',
            (project_code, entry_id)
        )
        conn.commit()
        conn.close()

        # Redirect to avoid resubmitting the form
        return redirect(url_for('view_repotree'))

    # Fetch the employees managed by the current user
    conn = get_db_connection()
    repotree_employees = conn.execute(
        'SELECT * FROM EMS_users WHERE ManagerID = ?',
        (current_user.id,)
    ).fetchall()

    if not repotree_employees:
        conn.close()
        return redirect(url_for('home'))

    # Fetch timesheet entries for all managed employees
    employee_ids = [employee['EmployeeID'] for employee in repotree_employees]
    placeholders = ', '.join(['?'] * len(employee_ids))
    timesheet_entries = conn.execute(
        f'SELECT * FROM timesheet_entries WHERE employee_id IN ({placeholders})  order by date DESC ',
        employee_ids
    ).fetchall()

    # Fetch the entry for editing if an ID is provided
    if edit_entry_id:
        edit_entry = conn.execute(
            'SELECT * FROM timesheet_entries WHERE entree_id = ?',
            (edit_entry_id,)
        ).fetchone()

    conn.close()
    return render_template('view_repotree.html', employees=repotree_employees, timesheets=timesheet_entries, edit_entry=edit_entry, id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)

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
    return render_template('success.html',id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)







from datetime import datetime, timedelta

@app.route('/view_summary', methods=['GET'])
@login_required
def view_summary():
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    current_date = datetime.strptime(selected_date, '%Y-%m-%d')

    # Calculate the start and end dates for the week
    weekday_index = current_date.weekday()
    start_date = current_date - timedelta(days=weekday_index)
    end_date = start_date + timedelta(days=6)

    # Initialize the summary dictionary
    summary = {
        "dates": {f"{(start_date + timedelta(days=i)).strftime('%Y-%m-%d')}": {
            "day": (start_date + timedelta(days=i)).strftime('%a'),  
            "billable": 0,
            "nonbillable_admin_time": 0,
            "nonbillable_training_time": 0,
            "non-billable": 0,
            "unavailable_time": 0,
            "total_time": 0
        } for i in range(7)},
        "totals": {
            "billable": 0,
            "nonbillable_admin_time": 0,
            "nonbillable_training_time": 0,
            "non-billable": 0,
            "unavailable_time": 0,
            "total_time": 0
        }
    }

    try:
        conn = get_db_connection()
        entries = conn.execute(
            '''SELECT * FROM timesheet_entries 
               WHERE date BETWEEN ? AND ? AND employee_id = ?''',
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), current_user.id)
        ).fetchall()
        conn.close()

        # Process each entry
        for entry in entries:
            date = entry['date']
            billable_time = entry['billable_time']
            nonbillable_admin_time = entry['nonbillable_admin_time']
            nonbillable_training_time = entry['nonbillable_training_time']
            unavailable_time = entry['unavailable_time']
            total_time = entry['total_time']

            # Update the day's summary
            day_summary = summary['dates'][date]
            day_summary['billable'] += billable_time
            day_summary['nonbillable_admin_time'] += nonbillable_admin_time
            day_summary['nonbillable_training_time'] += nonbillable_training_time
            day_summary['non-billable'] += nonbillable_admin_time + nonbillable_training_time
            day_summary['unavailable_time'] += unavailable_time
            day_summary['total_time'] += total_time

            # Update the totals
            summary['totals']['billable'] += billable_time
            summary['totals']['nonbillable_admin_time'] += nonbillable_admin_time
            summary['totals']['nonbillable_training_time'] += nonbillable_training_time
            summary['totals']['non-billable'] += nonbillable_admin_time + nonbillable_training_time
            summary['totals']['unavailable_time'] += unavailable_time
            summary['totals']['total_time'] += total_time

    except Exception as e:
        flash(f"An error occurred while fetching the summary: {str(e)}", 'error')
        return redirect(url_for('home'))

    # Render the template with the updated summary
    return render_template('view_summary.html', summary=summary, start_date=start_date.strftime('%Y-%m-%d'), id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)




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





@app.route('/view_entries_by_date/<date>', methods=['GET'])
@login_required
def view_entries_by_date(date):
    try:
        conn = get_db_connection()
        entries = conn.execute(
            'SELECT * FROM timesheet_entries WHERE date = ? AND employee_id = ?',
            (date, current_user.id)
        ).fetchall()
        conn.close()
    except Exception as e:
        return redirect(url_for('view_summary'))

    return render_template('view_entries_by_date.html', entries=entries, date=date, id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)






# Route to render the edit entry form
@app.route('/edit_entry/<int:entry_id>', methods=['GET'])
@login_required
def edit_entry(entry_id):
    try:
        conn = get_db_connection()
        entry = conn.execute(
            'SELECT * FROM timesheet_entries WHERE entree_id = ? AND employee_id = ?',
            (entry_id, current_user.id)
        ).fetchone()
        conn.close()
        if not entry:
            return redirect(url_for('view_summary'))

        # Convert to dictionary for easier debugging
        entry_dict = dict(entry)
        print(f"Entry data: {entry_dict}")  # Print as dictionary
    except Exception as e:
        return redirect(url_for('view_summary'))

    return render_template('edit_entry.html', entry=entry, id =current_user.id, fname=current_user.fname, lname=current_user.lname, role=current_user.role, team=current_user.team ,managername=current_user.managername)



# Route to handle updating the entry
@app.route('/update_entry/<int:entry_id>', methods=['POST'])
@login_required
def update_entry(entry_id):
    try:
        # Get form data safely
        duration_hours = int(request.form.get('duration_hours', 0))
        duration_minutes = int(request.form.get('duration_minutes', 0))
        total_time = round(duration_hours + (duration_minutes / 60), 2)
        allocation_type = request.form.get('allocation_type', '')
        category_1 = request.form.get('category_1', '')
        category_2 = request.form.get('category_2', '')
        category_3 = request.form.get('category_3', '')
        comments = request.form.get('comments', '')

        # Update the database entry
        conn = get_db_connection()
        conn.execute('''
            UPDATE timesheet_entries
            SET duration_hours = ?, duration_minutes = ?, total_time = ?, 
                allocation_type = ?, category_1 = ?, category_2 = ?, category_3 = ?, comments = ?
            WHERE entree_id = ? AND employee_id = ?
        ''', (duration_hours, duration_minutes, total_time, allocation_type, category_1, category_2, category_3, comments, entry_id, current_user.id))
        conn.commit()
        conn.close()
      
    except Exception as e:
        flash(f'Error occurred while updating entry: {str(e)}', 'error')

    # Redirect back to the view for this date's entries
    return redirect(url_for('view_entries_by_date', date=request.form.get('date')))




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
    return redirect(url_for('view_summary'))




if __name__ == "__main__":
    app.run(debug=True,port=5001)
