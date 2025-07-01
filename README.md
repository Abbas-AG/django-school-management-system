---

# 🏫 Django School Management System

A full-featured web application built with **Django** to manage daily school operations — students, teachers, classes, attendance, grades, announcements, and more.

---

## 🌟 Features

* **Multi-role Authentication**: Separate access for **admins**, **teachers**, and **students**.
* **Dashboard**: Quick overview of attendance, grades, and notifications.
* **Student & Teacher Management**: Add/edit/delete profiles, manage class assignments.
* **Class & Subject Management**: Create classes, subjects and assign teachers/students.
* **Attendance Tracking**: Record and review daily attendance.
* **Gradebook**: Enter and track student grades per subject.
* **Announcements**: Broadcast messages to selected user groups.

---

this is a yourube video to show the project: https://youtu.be/cwLQFFRQ3yo

## 🔧 Installation Guide

### Recommended Setup

```bash
# Clone the project
git clone https://github.com/Abbas-AG/django-school-management-system.git
cd django-school-management-system

# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create an admin/superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the app and `http://127.0.0.1:8000/admin/` for Django’s admin interface using your superuser.

---

## 🧩 Project Structure

```
├── manage.py
├── requirements.txt
├── student_management_app/
│   ├── models.py       # Definitions for Students, Teachers, Subjects, etc.
│   ├── views.py        # Controller logic for CRUD operations
│   ├── templates/      # HTML templates for dashboards and forms
│   └── static/         # CSS, JS, images
└── student_management_system/  # Project settings and URLs
```

---

## ⚙️ Key Components

1. **Authentication & Roles**
   Utilizes Django’s auth system with custom user roles.

2. **CRUD Operations**
   Manage students, teachers, classes, subjects, and attendance.

3. **Grade & Attendance Management**
   Teachers can record, edit, and view grades/attendance reports.

4. **Announcement System**
   Admins or teachers can post updates visible on dashboards.

---

## 🎯 Usage

1. Log in as **Admin** — create/manage users, classes, subjects, attendance, grades, and announcements.
2. Log in as **Teacher** — view assigned classes, record attendance, grades, and post announcements.
3. Log in as **Student** — view your classes, attendance records, grades, and announcements.

---

## 🛠️ Contributing

* Create issues or pull requests as needed.
* Follow PEP 8 style; please document your code.
* Run tests (if included) before submitting.

---

## 📜 License

This project is made by me with some help from @sumitkumar1503 on github.

---

## 🙋 Questions?

Feel free to open an issue or reach out via telegram: @ENG_AG.

---
