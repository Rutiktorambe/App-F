| EmployeeID | Fname     | Mname | Lname     | ManagerID | EMSlogin | Role                   | Team       | ManagerName | Password | Email                    |
| ---------- | --------- | ----- | --------- | --------- | -------- | ---------------------- | ---------- | ----------- | -------- | ------------------------ |
| 101        | John      | A     | Doe       | 103       | 101      | Software Engineer      | Technology | Alice Smith | pass     | JohnDoe@rsa.com          |
| 102        | Jane      |       | Smith     | 103       | 102      | Data Analyst           | Analytics  | Alice Smith | pass     | JaneSmith@rsa.com        |
| 103        | Alice     |       | Smith     | 105       | 103      | Team Lead              | Technology | Bob Johnson | pass     | AliceSmith@rsa.com       |
| 104        | David     | B     | Lee       | 106       | 104      | Project Manager        | Management | Eva Garcia  | pass     | DavidLee@rsa.com         |
| 105        | Bob       |       | Johnson   | NULL      | 105      | CTO                    | Executive  | NULL        | pass     | BobJohnson@rsa.com       |
| 106        | Eva       |       | Garcia    | 105       | 106      | Head of Management     | Management | Bob Johnson | pass     | EvaGarcia@rsa.com        |
| 107        | Michael   | C     | Brown     | 103       | 107      | Software Engineer      | Technology | Alice Smith | pass     | MichaelBrown@rsa.com     |
| 108        | Emily     |       | Wilson    | 106       | 108      | Project Coordinator    | Management | Eva Garcia  | pass     | EmilyWilson@rsa.com      |
| 109        | Daniel    |       | Jones     | 103       | 109      | QA Engineer            | Technology | Alice Smith | pass     | DanielJones@rsa.com      |
| 110        | Olivia    | D     | Davis     | 106       | 110      | Project Manager        | Management | Eva Garcia  | pass     | OliviaDavis@rsa.com      |
| 111        | James     |       | Rodriguez | 103       | 111      | Software Engineer      | Technology | Alice Smith | pass     | JamesRodriguez@rsa.com   |
| 112        | Sophia    |       | Martinez  | 106       | 112      | Project Coordinator    | Management | Eva Garcia  | pass     | SophiaMartinez@rsa.com   |
| 113        | William   | E     | Taylor    | 103       | 113      | UI/UX Designer         | Technology | Alice Smith | pass     | WilliamTaylor@rsa.com    |
| 114        | Isabella  |       | Anderson  | 106       | 114      | Project Manager        | Management | Eva Garcia  | pass     | IsabellaAnderson@rsa.com |
| 115        | Ethan     |       | Thomas    | 103       | 115      | DevOps Engineer        | Technology | Alice Smith | pass     | EthanThomas@rsa.com      |
| 116        | Mia       | F     | Jackson   | 106       | 116      | Project Coordinator    | Management | Eva Garcia  | pass     | MiaJackson@rsa.com       |
| 117        | Alexander |       | White     | 103       | 117      | Software Engineer      | Technology | Alice Smith | pass     | AlexanderWhite@rsa.com   |
| 118        | Ava       |       | Harris    | 106       | 118      | Project Manager        | Management | Eva Garcia  | pass     | AvaHarris@rsa.com        |
| 119        | Matthew   | G     | Martin    | 103       | 119      | Database Administrator | Technology | Alice Smith | pass     | MatthewMartin@rsa.com    |
| 120        | Chloe     |       | Thompson  | 106       | 120      | Project Coordinator    | Management | Eva Garcia  | pass     | ChloeThompson@rsa.com    |

## SQL Query

```SQL
CREATE TABLE EMS_users (
    EmployeeID INT PRIMARY KEY,
    Fname VARCHAR(50),
    Mname VARCHAR(50),
    Lname VARCHAR(50),
    ManagerID INT,
    EMSlogin VARCHAR(50),
    Role VARCHAR(100),
    Team VARCHAR(50),
    ManagerName VARCHAR(100),
    Password VARCHAR(50),
    Email VARCHAR(255)
);

INSERT INTO EMS_users (EmployeeID, Fname, Mname, Lname, ManagerID, EMSlogin, Role, Team, ManagerName, Password, Email)
VALUES
(101, 'John', 'A', 'Doe', 103, '101', 'Software Engineer', 'Technology', 'Alice Smith', 'pass', 'JohnDoe@rsa.com'),
(102, 'Jane', NULL, 'Smith', 103, '102', 'Data Analyst', 'Analytics', 'Alice Smith', 'pass', 'JaneSmith@rsa.com'),
(103, 'Alice', NULL, 'Smith', 105, '103', 'Team Lead', 'Technology', 'Bob Johnson', 'pass', 'AliceSmith@rsa.com'),
(104, 'David', 'B', 'Lee', 106, '104', 'Project Manager', 'Management', 'Eva Garcia', 'pass', 'DavidLee@rsa.com'),
(105, 'Bob', NULL, 'Johnson', NULL, '105', 'CTO', 'Executive', NULL, 'pass', 'BobJohnson@rsa.com'),
(106, 'Eva', NULL, 'Garcia', 105, '106', 'Head of Management', 'Management', 'Bob Johnson', 'pass', 'EvaGarcia@rsa.com'),
(107, 'Michael', 'C', 'Brown', 103, '107', 'Software Engineer', 'Technology', 'Alice Smith', 'pass', 'MichaelBrown@rsa.com'),
(108, 'Emily', NULL, 'Wilson', 106, '108', 'Project Coordinator', 'Management', 'Eva Garcia', 'pass', 'EmilyWilson@rsa.com'),
(109, 'Daniel', NULL, 'Jones', 103, '109', 'QA Engineer', 'Technology', 'Alice Smith', 'pass', 'DanielJones@rsa.com'),
(110, 'Olivia', 'D', 'Davis', 106, '110', 'Project Manager', 'Management', 'Eva Garcia', 'pass', 'OliviaDavis@rsa.com'),
(111, 'James', NULL, 'Rodriguez', 103, '111', 'Software Engineer', 'Technology', 'Alice Smith', 'pass', 'JamesRodriguez@rsa.com'),
(112, 'Sophia', NULL, 'Martinez', 106, '112', 'Project Coordinator', 'Management', 'Eva Garcia', 'pass', 'SophiaMartinez@rsa.com'),
(113, 'William', 'E', 'Taylor', 103, '113', 'UI/UX Designer', 'Technology', 'Alice Smith', 'pass', 'WilliamTaylor@rsa.com'),
(114, 'Isabella', NULL, 'Anderson', 106, '114', 'Project Manager', 'Management', 'Eva Garcia', 'pass', 'IsabellaAnderson@rsa.com'),
(115, 'Ethan', NULL, 'Thomas', 103, '115', 'DevOps Engineer', 'Technology', 'Alice Smith', 'pass', 'EthanThomas@rsa.com'),
(116, 'Mia', 'F', 'Jackson', 106, '116', 'Project Coordinator', 'Management', 'Eva Garcia', 'pass', 'MiaJackson@rsa.com'),
(117, 'Alexander', NULL, 'White', 103, '117', 'Software Engineer', 'Technology', 'Alice Smith', 'pass', 'AlexanderWhite@rsa.com'),
(118, 'Ava', NULL, 'Harris', 106, '118', 'Project Manager', 'Management', 'Eva Garcia', 'pass', 'AvaHarris@rsa.com'),
(119, 'Matthew', 'G', 'Martin', 103, '119', 'Database Administrator', 'Technology', 'Alice Smith', 'pass', 'MatthewMartin@rsa.com'),
(120, 'Chloe', NULL, 'Thompson', 106, '120', 'Project Coordinator', 'Management', 'Eva Garcia', 'pass', 'ChloeThompson@rsa.com');
```
