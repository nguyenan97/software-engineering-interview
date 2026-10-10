SELECT d.Name, COUNT(e.Name) AS EmployeeCount
FROM Department AS d
LEFT JOIN Employee AS e ON e.DepartmentId = d.DepartmentId
GROUP BY d.Name
HAVING COUNT(e.Name) > 3
ORDER BY d.Name;
