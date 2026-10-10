```sql
SELECT d.DepartmentId, d.Name, COUNT(e.EmployeeId) AS EmployeeCount
FROM Department AS d
INNER JOIN Employee AS e ON e.DepartmentId = d.DepartmentId
GROUP BY d.DepartmentId, d.Name
HAVING COUNT(e.EmployeeId) > 3
ORDER BY d.DepartmentId;
```
