'''password
HYDRAxJonathan
Latur@4255
````

sqlite3 ems_users.db

.tables

.schema EMS_users

.schema timesheet_entries

.headers on
.mode csv
.output EMS_users.csv
SELECT * FROM EMS_users;
.output stdout
.output timesheet_entries.csv
SELECT * FROM timesheet_entries;
.output stdout

.mode csv
.import EMS_users.csv EMS_users
.import timesheet_entries.csv timesheet_entries

SELECT * FROM EMS_users;
SELECT * FROM timesheet_entries;

.quit
