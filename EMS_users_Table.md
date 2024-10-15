| EmployeeID | Fname | Mname | Lname | ManagerID | EMSlogin | Role | Team | ManagerName | Password |
|------------|-----------|-------|------------|-----------|-------------|----------------------|-------------|---------------|----------|
| 101 | John | A | Doe | 103 | jdoe | Software Engineer | Technology | Alice Smith | pass |
| 102 | Jane | | Smith | 103 | jsmith | Data Analyst | Analytics | Alice Smith | pass |
| 103 | Alice | | Smith | 105 | asmith | Team Lead | Technology | Bob Johnson | pass |
| 104 | David | B | Lee | 106 | dlee | Project Manager | Management | Eva Garcia | pass |
| 105 | Bob | | Johnson | NULL | bjohnson | CTO | Executive | NULL | pass |
| 106 | Eva | | Garcia | 105 | egarcia | Head of Management | Management | Bob Johnson | pass |
| 107 | Michael | C | Brown | 103 | mbrown | Software Engineer | Technology | Alice Smith | pass |
| 108 | Emily | | Wilson | 106 | ewilson | Project Coordinator | Management | Eva Garcia | pass |
| 109 | Daniel | | Jones | 103 | djones | QA Engineer | Technology | Alice Smith | pass |
| 110 | Olivia | D | Davis | 106 | odavis | Project Manager | Management | Eva Garcia | pass |
| 111 | James | | Rodriguez | 103 | jrodriguez | Software Engineer | Technology | Alice Smith | pass |
| 112 | Sophia | | Martinez | 106 | smartinez | Project Coordinator | Management | Eva Garcia | pass |
| 113 | William | E | Taylor | 103 | wtaylor | UI/UX Designer | Technology | Alice Smith | pass |
| 114 | Isabella | | Anderson | 106 | ianderson | Project Manager | Management | Eva Garcia | pass |
| 115 | Ethan | | Thomas | 103 | ethomas | DevOps Engineer | Technology | Alice Smith | pass |
| 116 | Mia | F | Jackson | 106 | mjackson | Project Coordinator | Management | Eva Garcia | pass |
| 117 | Alexander | | White | 103 | awhite | Software Engineer | Technology | Alice Smith | pass |
| 118 | Ava | | Harris | 106 | aharris | Project Manager | Management | Eva Garcia | pass |
| 119 | Matthew | G | Martin | 103 | mmartin | Database Administrator| Technology | Alice Smith | pass |
| 120 | Chloe | | Thompson | 106 | cthompson | Project Coordinator | Management | Eva Garcia | pass |

 DELETE FROM ems_users where EmployeeID > 1000