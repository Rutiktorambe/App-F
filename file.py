# import sqlite3 # conn = sqlite3.connect('ems_user.db') # Make sure this
matches the path used in the app # c = conn.cursor() # # Create the EMS_users
table # c.execute(''' # CREATE TABLE IF NOT EXISTS EMS_users ( # EmployeeID TEXT
PRIMARY KEY, # Fname TEXT, # Mname TEXT, # Lname TEXT, # ManagerID TEXT, #
EMSlogin TEXT, # Role TEXT, # Team TEXT, # ManagerName TEXT, # Password TEXT # )
# ''') # # Insert some sample data # c.execute("INSERT INTO EMS_users
(EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName,
Password) VALUES ('1001', 'Alice', 'J.', 'Lee', '1000', '1001', 'Analyst', 'IT',
'John Smith', 'pass')") # c.execute("INSERT INTO EMS_users (EmployeeID, Fname,
Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES
('1002', 'Brian', 'K.', 'Jones', '1001', '1002', 'SDE1', 'HE', 'Alice Lee',
'pass')") # c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname,
ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1003',
'Charlie', 'A.', 'Brown', '1001', '1003', 'Designer', 'UX', 'Alice Lee',
'pass')") # c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname,
ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1004', 'David',
'B.', 'Wilson', '1002', '1004', 'Developer', 'IT', 'Brian Jones', 'pass')") #
conn.commit() # conn.close() import sqlite3 # Connect to the database (or create
it if it doesn't exist) conn = sqlite3.connect('ems_user.db') c = conn.cursor()
# Create timesheet_entries table if it doesn't exist c.execute(''' CREATE TABLE
IF NOT EXISTS timesheet_entries ( entree_id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id TEXT, fname TEXT, lname TEXT, team TEXT, manager_name TEXT, date
TEXT, duration_hours INTEGER, duration_minutes INTEGER, total_time REAL,
project_code TEXT, allocation_type TEXT, holiday_status TEXT, category_1 TEXT,
category_2 TEXT, category_3 TEXT, comments TEXT ) ''') # Commit the changes and
close the connection conn.commit() conn.close() # CREATE TABLE IF NOT EXISTS
timesheet_entries ( # entree_id INTEGER PRIMARY KEY AUTOINCREMENT, # employee_id
TEXT, # fname TEXT, # lname TEXT, # team TEXT, # manager_name TEXT, # date TEXT,
# duration_hours INTEGER, # duration_minutes INTEGER, # billable_time REAL, #
nonbillable_admin_time REAL, # nonbillable_training_time REAL, #
unavailable_time Real, # total_time REAL, # project_code TEXT, # allocation_type
TEXT, # holiday_status TEXT, # category_1 TEXT, # category_2 TEXT, # category_3
TEXT, # comments TEXT # ) entree_id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id TEXT, fname TEXT, lname TEXT, team TEXT, manager_name TEXT, date
TEXT, duration_hours INTEGER, duration_minutes INTEGER, billable_time REAL,
nonbillable_admin_time REAL, nonbillable_training_time REAL, unavailable_time
Real, total_time REAL, project_code TEXT, allocation_type TEXT, holiday_status
TEXT, category_1 TEXT, category_2 TEXT, category_3 TEXT, comments TEXT

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Weekly Summary</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='css/timesheet/view_summary.css') }}"
    />
  </head>
  <body>
    {% include 'navbar.html' %}
    <div class="summary-box">
      <nav class="ts-nav-container">
        <div class="ts-nav-center">
          <a href="/timesheet_home" class="ts-nav-link">Timesheet</a>
          <a href="/fill_timesheet" class="ts-nav-link">Fill Timesheet</a>
        </div>
      </nav>
      <div class="ts-summary-container">
        <h1 class="ts-summary-title">Weekly Summary</h1>
        <form
          action="{{ url_for('view_summary') }}"
          method="get"
          class="ts-summary-form"
        >
          <input
            type="date"
            name="date"
            value="{{ start_date }}"
            required
            class="ts-summary-date-input"
          />
          <button type="submit" class="ts-summary-button">Show Week</button>
        </form>
        <table class="ts-summary-table">
          <thead>
            <tr>
              <th class="ts-summary-header">Date</th>
              <th class="ts-summary-header">Day</th>
              <th class="ts-summary-header">Billable</th>
              <th class="ts-summary-header">Admin</th>
              <th class="ts-summary-header">Training</th>
              <th class="ts-summary-header">Non-billable</th>
              <th class="ts-summary-header">Unavailable Time</th>
              <th class="ts-summary-header">Total Time</th>
            </tr>
          </thead>
          <tbody>
            {% if summary.dates %} {% for date, details in summary.dates.items()
            %}
            <tr>
              <td class="ts-summary-data">
                <a
                  href="{{ url_for('view_entries_by_date', date=date) }}"
                  class="ts-summary-link"
                  >{{ date }}</a
                >
              </td>
              <td class="ts-summary-data">{{ details['day'] }}</td>
              <td class="ts-summary-data">{{ details['billable'] }}</td>
              <td class="ts-summary-data">
                {{ details['nonbillable_admin_time'] }}
              </td>
              <td class="ts-summary-data">
                {{ details['nonbillable_training_time'] }}
              </td>
              <td class="ts-summary-data">{{ details['non-billable'] }}</td>
              <td class="ts-summary-data">{{ details['unavailable_time'] }}</td>
              <td class="ts-summary-data">{{ details['total_time'] }}</td>
            </tr>
            {% endfor %} {% else %}
            <tr>
              <td colspan="8" class="ts-summary-no-data">
                No entries found for this week.
              </td>
            </tr>
            {% endif %}
          </tbody>
        </table>
      </div>
    </div>
  </body>
</html>
