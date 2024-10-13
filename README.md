# App-F

Method 1: Using SQLite Command Line
Open the Command Line Interface:

For Windows, open the Command Prompt.
For macOS/Linux, open the Terminal.
Access SQLite:

Run the following command to start the SQLite command line interface:
bash
Copy code
sqlite3 ems_users.db
List Tables:

To see the tables in the database, use:
sql
Copy code
.tables
View Table Structure:

To see the structure of a specific table (replace table_name with the actual table name):
sql
Copy code
.schema table_name
Query Data:

To select data from a table (replace table_name with the actual table name):
sql
Copy code
SELECT \* FROM table_name;
Export Data (Optional):

You can export data to a CSV file:
sql
Copy code
.headers on
.mode csv
.output output_file.csv
SELECT \* FROM table_name;
.output stdout
Exit SQLite:

Type .exit to leave the SQLite command line interface.
