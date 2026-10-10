```sql
CREATE TABLE Department (
    DepartmentId INT NOT NULL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL
);
CREATE TABLE Employee (
    EmployeeId INT NOT NULL PRIMARY KEY,
    DepartmentId INT NOT NULL REFERENCES Department(DepartmentId),
    Name VARCHAR(50) NULL,
    IsActive INT NOT NULL CHECK (IsActive IN (0, 1))
);
INSERT INTO Department (DepartmentId, Name) VALUES
    (10, 'Platform'), (20, 'Platform'), (30, 'Support');
INSERT INTO Employee (EmployeeId, DepartmentId, Name, IsActive) VALUES
    (101, 10, 'A', 1), (102, 10, 'B', 1),
    (103, 10, 'C', 1), (104, 10, NULL, 0),
    (201, 20, 'D', 1), (202, 20, 'E', 1), (203, 20, 'F', 1);
```
