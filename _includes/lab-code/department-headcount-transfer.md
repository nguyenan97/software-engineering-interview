```sql
SELECT d.DepartmentId, d.Name, COUNT(e.EmployeeId) AS EmployeeCount
FROM Department AS d
LEFT JOIN Employee AS e
    ON e.DepartmentId = d.DepartmentId AND e.IsActive = 1
GROUP BY d.DepartmentId, d.Name
ORDER BY d.DepartmentId;
```
