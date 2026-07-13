# Employee Leave Management System

The Kiran Academy assignment project for managing employees and leave applications using Django, Django REST Framework, MySQL, HTML, CSS, and Bootstrap.

## Features

- Employee CRUD: add, view, update, and delete employees.
- Leave CRUD: apply leave, view leave history, update status, and delete leave.
- Dashboard counts: total employees, total leave applications, pending, approved, and rejected.
- Search employees by name or employee ID.
- Filter leaves by status and leave type.
- REST APIs for employees and leaves.
- Validation for required fields, email, mobile number, and leave date range.
- Bootstrap UI, pagination, login, and logout.
- Role based authorization: HR can manage employees and approve/reject leaves, employees can apply and view their own leave history.

## Technologies

- Python 3
- Django
- Django REST Framework
- MySQL
- HTML, CSS, Bootstrap
- Git and GitHub

## Setup

1. Create and activate a virtual environment.
2. Install packages:

```bash
pip install -r requirements.txt
```

3. Create a MySQL database:

```sql
CREATE DATABASE employee_leave_db;
```

4. Update database username and password in `EmployeeLeaveManagement/settings.py` if needed.
5. Run migrations:

```bash
python manage.py migrate
```

6. Create an admin user:

```bash
python manage.py createsuperuser
```

7. Start the server:

```bash
python manage.py runserver
```

## Website URLs

- Dashboard: `/`
- Employee List: `/list/`
- Add Employee: `/add/`
- Leave List: `/leave-list/`
- Apply Leave: `/apply/`
- Login: `/accounts/login/`
- Register: `/register/`
- Admin: `/admin/`

## REST API URLs

Employee APIs:

- `GET /api/employees/`
- `GET /api/employees/<id>/`
- `POST /api/employees/`
- `PUT /api/employees/<id>/`
- `DELETE /api/employees/<id>/`

Leave APIs:

- `GET /api/leaves/`
- `GET /api/leaves/<id>/`
- `POST /api/leaves/`
- `PUT /api/leaves/<id>/`
- `DELETE /api/leaves/<id>/`

## Validation

- Employee ID, name, email, department, mobile, and joining date are required.
- Email uses Django `EmailField`.
- Mobile number must be 10 digits and start with 6, 7, 8, or 9.
- From date cannot be greater than to date.
- Leave status uses fixed choices: Pending, Approved, Rejected.
- Leave type uses fixed choices: Casual, Sick, Earned.

## ER Diagram

See `docs/ER_DIAGRAM.md`.

## Postman Collection

Import `postman/EmployeeLeaveManagement.postman_collection.json` into Postman.
