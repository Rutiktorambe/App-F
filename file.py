

import sqlite3

conn = sqlite3.connect('ems_user.db')  # Make sure this matches the path used in the app
c = conn.cursor()

# Create the EMS_users table
c.execute('''
CREATE TABLE IF NOT EXISTS EMS_users (
    EmployeeID TEXT PRIMARY KEY,
    Fname TEXT,
    Mname TEXT,
    Lname TEXT,
    ManagerID TEXT,
    EMSlogin TEXT,
    Role TEXT,
    Team TEXT,
    ManagerName TEXT,
    Password TEXT
)
''')

# Insert some sample data
c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1001', 'Alice', 'J.', 'Lee', '1000', '1001', 'Analyst', 'IT', 'John Smith', 'pass')")
c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1002', 'Brian', 'K.', 'Jones', '1001', '1002', 'SDE1', 'HE', 'Alice Lee', 'pass')")
c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1003', 'Charlie', 'A.', 'Brown', '1001', '1003', 'Designer', 'UX', 'Alice Lee', 'pass')")
c.execute("INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password) VALUES ('1004', 'David', 'B.', 'Wilson', '1002', '1004', 'Developer', 'IT', 'Brian Jones', 'pass')")

conn.commit()
conn.close()
