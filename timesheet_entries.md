| entree_id | employee_id | fname | lname | team       | manager_name | date       | duration_hours | duration_minutes | billable_time | nonbillable_admin_time | nonbillable_training_time | unavailable_time | total_time | project_code | allocation_type | holiday_status | category_1 | category_2 | category_3 | comments |
| --------- | ----------- | ----- | ----- | ---------- | ------------ | ---------- | -------------- | ---------------- | ------------- | ---------------------- | ------------------------- | ---------------- | ---------- | ------------ | --------------- | -------------- | ---------- | ---------- | ---------- | -------- |
| 1         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-15 | 8              | 10               | 8.17          | 0.0                    | 0.0                       | 0.0              | 8.17       |              | Billable        |                | Cat B1     |            |            | thif     |
| 2         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-16 | 8              | 10               | 8.17          | 0.0                    | 0.0                       | 0.0              | 8.17       |              | billable        |                | cat_b1     |            |            |          |
| 3         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-09 | 2              | 20               | 0.0           | 2.33                   | 0.0                       | 0.0              | 2.33       |              | non-billable    |                | admin      |            |            | the      |
| 4         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-08 | 2              | 20               | 0.0           | 2.33                   | 0.0                       | 0.0              | 2.33       |              | non-billable    |                | admin      |            |            | the      |
| 5         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-15 | 7              | 5                | 0.0           | 0.0                    | 7.08                      | 0.0              | 7.08       |              | non-billable    |                | training   |            |            |          |
| 6         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-16 | 7              | 5                | 0.0           | 0.0                    | 7.08                      | 0.0              | 7.08       |              | non-billable    |                | training   |            |            |          |
| 7         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-08 | 7              | 5                | 0.0           | 0.0                    | 7.08                      | 0.0              | 7.08       |              | non-billable    |                | training   |            |            |          |
| 8         | 102         | Jane  | Smith | Analytics  | Alice Smith  | 2024-10-09 | 7              | 5                | 0.0           | 0.0                    | 7.08                      | 0.0              | 7.08       |              | non-billable    |                | training   |            |            |          |
| 9         | 101         | John  | Doe   | Technology | Alice Smith  | 2024-10-15 | 5              | 15               | 0.0           | 0.0                    | 5.25                      | 0.0              | 5.25       |              | non-billable    |                | training   |            | dummy_1    | Trail    |
| 10        | 101         | John  | Doe   | Technology | Alice Smith  | 2024-10-10 | 5              | 15               | 0.0           | 0.0                    | 5.25                      | 0.0              | 5.25       |              | non-billable    |                | training   |            | dummy_1    | Trail    |
| 11        | 101         | John  | Doe   | Technology | Alice Smith  | 2024-10-14 | 5              | 15               | 0.0           | 0.0                    | 5.25                      | 0.0              | 5.25       |              | non-billable    |                | training   |            | dummy_1    | Trail    |
| 12        | 101         | John  | Doe   | Technology | Alice Smith  | 2024-10-17 | 5              | 15               | 0.0           | 0.0                    | 5.25                      | 0.0              | 5.25       |              | non-billable    |                | training   |            | dummy_1    | Trail    |

```bash


CREATE TABLE timesheet_entries (
    unique_number INT AUTO_INCREMENT,
    entree_id VARCHAR(255) PRIMARY KEY,
    employee_id VARCHAR(50),
    fname VARCHAR(100),
    lname VARCHAR(100),
    team VARCHAR(50),
    manager_name VARCHAR(100),
    date VARCHAR(50),
    duration_hours INTEGER,
    duration_minutes INTEGER,
    billable_time REAL,
    nonbillable_admin_time REAL,
    nonbillable_training_time REAL,
    unavailable_time REAL,
    total_time REAL,
    project_code VARCHAR(50),
    allocation_type VARCHAR(50),
    holiday_status VARCHAR(50),
    category_1 VARCHAR(50),
    category_2 VARCHAR(50),
    category_3 VARCHAR(50),
    comments VARCHAR(50),
    entry_timestamp REAL,
    CONSTRAINT unique_combination UNIQUE (unique_number, fname, lname, employee_id, entry_timestamp));

```
