# import sqlite3

# conn = sqlite3.connect('ems_user.db')  # Make sure this matches the path used in the app
# c = conn.cursor()

# # Create the EMS_users table
# c.execute('''
# CREATE TABLE IF NOT EXISTS EMS_users (
#     EmployeeID TEXT PRIMARY KEY,
#     Fname TEXT,
#     Mname TEXT,
#     Lname TEXT,
#     ManagerID TEXT,
#     EMSlogin TEXT,
#     Role TEXT,
#     Team TEXT,
#     ManagerName TEXT,
#     Password TEXT
# )
# ''')

# # Insert some sample data
# c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1001', 'Alice', 'J.', 'Lee', '1000', '1001', 'Analyst', 'IT', 'John Smith', 'pass')")
# c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1002', 'Brian', 'K.', 'Jones', '1001', '1002', 'SDE1', 'HE', 'Alice Lee', 'pass')")
# c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1003', 'Charlie', 'A.', 'Brown', '1001', '1003', 'Designer', 'UX', 'Alice Lee', 'pass')")
# c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1004', 'David', 'B.', 'Wilson', '1002', '1004', 'Developer', 'IT', 'Brian Jones', 'pass')")

# conn.commit()
# conn.close()

import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('ems_user.db')
c = conn.cursor()

# Create timesheet_entries table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS timesheet_entries (
    entree_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    fname TEXT,
    lname TEXT,
    team TEXT,
    manager_name TEXT,
    date TEXT,
    duration_hours INTEGER,
    duration_minutes INTEGER,
    total_time REAL,
    project_code TEXT,
    allocation_type TEXT,
    holiday_status TEXT,
    category_1 TEXT,
    category_2 TEXT,
    category_3 TEXT,
    comments TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()


# CREATE TABLE IF NOT EXISTS timesheet_entries (
#     entree_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     employee_id TEXT,
#     fname TEXT,
#     lname TEXT,
#     team TEXT,
#     manager_name TEXT,
#     date TEXT,
#     duration_hours INTEGER,
#     duration_minutes INTEGER,
#     billable_time REAL,
#     nonbillable_admin_time REAL,
#     nonbillable_training_time REAL,
#     unavailable_time Real,
#     total_time REAL,
#     project_code TEXT,
#     allocation_type TEXT,
#     holiday_status TEXT,
#     category_1 TEXT,
#     category_2 TEXT,
#     category_3 TEXT,
#     comments TEXT
# )


    entree_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    fname TEXT,
    lname TEXT,
    team TEXT,
    manager_name TEXT,
    date TEXT,
    duration_hours INTEGER,
    duration_minutes INTEGER,
    billable_time REAL,
    nonbillable_admin_time REAL,
    nonbillable_training_time REAL,
    unavailable_time Real,
    total_time REAL,
    project_code TEXT,
    allocation_type TEXT,
    holiday_status TEXT,
    category_1 TEXT,
    category_2 TEXT,
    category_3 TEXT,
    comments TEXT