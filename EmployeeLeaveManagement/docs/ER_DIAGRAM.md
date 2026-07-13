# ER Diagram

```text
+--------------------+             +----------------------+
| Employee           |             | Leave                |
+--------------------+             +----------------------+
| id (PK)            | 1         M | id (PK)              |
| employee_id UNIQUE |-------------| employee_id (FK)     |
| name               |             | leave_type           |
| email UNIQUE       |             | from_date            |
| department         |             | to_date              |
| mobile             |             | reason               |
| joining_date       |             | status               |
+--------------------+             | created_at           |
                                   | updated_at           |
                                   +----------------------+
```

Relationship:

- One employee can have many leave applications.
- Each leave application belongs to one employee.
