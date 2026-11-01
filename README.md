# 🎓 Project College - Academic Cloud Management System

[![Django Version](https://img.shields.io/badge/Django-6.1%2B-0C4B33?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/UI-HTML5%20%7C%20CSS3%20%7C%20FontAwesome%206-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://fontawesome.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A modern, role-based **College & Academic Management System** built with **Django**. Designed to streamline academic workflows for institutions, universities, and colleges with dedicated, secure portals for **Administrators**, **Teachers/Faculty**, and **Students**.

---

## 📌 Table of Contents

- [Key Features](#-key-features)
  - [🛡️ Admin Portal](#️-admin-portal)
  - [👨‍🏫 Faculty / Teacher Portal](#-faculty--teacher-portal)
  - [🎓 Student Portal](#-student-portal)
  - [📢 Shared Academic Features](#-shared-academic-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Architecture](#-project-architecture)
- [🚀 Quick Start & Installation](#-quick-start--installation)
  - [Prerequisites](#prerequisites)
  - [Setup Guide](#setup-guide)
- [🔑 Demo Accounts & Credentials](#-demo-accounts--credentials)
- [⚡ Custom Management Commands](#-custom-management-commands)
- [⚙️ Configuration & Production Deployment](#️-configuration--production-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Key Features

### 🛡️ Admin Portal
- **Executive Analytics Dashboard:** Instant overview of campus statistics (total students, faculties, departments, courses, pending leaves).
- **Student Management:** Register new students, assign roll numbers, departments, semesters, batches, and emergency guardian info.
- **Faculty Management:** Manage instructors, employee IDs, academic qualifications, and department affiliations.
- **Academic Hierarchy Setup:**
  - Create and manage **Departments** (e.g., Computer Science, IT, Mechanical).
  - Define **Degree Courses** (e.g., B.Tech, BCA, BSc CSIT) and semester counts.
  - Allocate **Subjects / Modules**, credit hours, and assign instructors.
- **Master Timetable Scheduler:** Build class schedules by assigning days, time slots, subjects, and lecture rooms.
- **Leave Request Administration:** Review, approve, or reject leave applications submitted by faculty and students with administrative remarks.
- **Notice Board Publisher:** Broadcast institutional announcements with pinning capabilities and role-specific audience targeting (*All, Students Only, Teachers Only*).

### 👨‍🏫 Faculty / Teacher Portal
- **Faculty Dashboard:** Personalized view of assigned subjects, daily timetable slots, and pending assignment reviews.
- **Smart Attendance Tracker:**
  - Mark daily subject attendance (*Present, Absent, Late*) with per-student remarks.
  - Interactive attendance logs and historical attendance reports.
- **Assignment Management:**
  - Create and publish assignments with deadlines, attachments, and maximum marks.
  - View incoming student submissions and download submitted work files.
  - Grade submissions and provide personalized constructive feedback.
- **Examination & Grade Book:**
  - Schedule exams with maximum and pass marks.
  - Bulk enter student marks with **automatic letter grade calculation** (`A+`, `A`, `B+`, `B`, `C`, `D`, `F`).
- **Personal Leave Applications:** Request time off and track status in real time.

### 🎓 Student Portal
- **Student Dashboard:** Real-time summary of attendance percentage, active assignments, and recent notices.
- **Interactive Timetable:** View weekly lecture schedules, assigned lecture halls, and instructor details.
- **Attendance Monitoring:** Detailed subject-wise breakdown of classes attended vs. total classes.
- **Assignment Hub:** Download course assignments, check submission deadlines, and submit files/text answers.
- **Exam Results & Report Card:** View marks obtained, maximum marks, calculated letter grades, and instructor remarks.
- **Leave Requests:** Submit absence requests directly to administration.

### 📢 Shared Academic Features
- **Role-Based Access Control (RBAC):** Tailored views and route protection based on user roles (`ADMIN`, `TEACHER`, `STUDENT`).
- **Profile Management:** View and edit contact details, addresses, and avatar images.
- **Responsive Modern UI:** Modern sidebar navigation, clean typography, glassmorphism cards, and mobile-friendly design.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | [Django 6.1+](https://www.djangoproject.com/) (Python) |
| **Authentication** | Django Custom `AbstractUser` with RBAC |
| **Database** | SQLite (default development) / PostgreSQL ready |
| **Frontend** | HTML5, CSS3 (Modular Styles), JavaScript (Vanilla) |
| **Iconography** | [FontAwesome 6](https://fontawesome.com/) |
| **File / Media Handling** | [Pillow](https://python-pillow.org/) (Uploads for profiles, assignments, submissions) |

---

## 📂 Project Architecture

```plaintext
College/
├── accounts/                  # Authentication & User Management App
│   ├── models.py              # Custom User, StudentProfile, TeacherProfile
│   ├── views.py               # Login, logout, profile & role redirects
│   └── urls.py                # Authentication endpoints
│
├── college_system/            # Project Configuration & Settings
│   ├── settings.py            # Global Django settings, auth models, apps
│   ├── urls.py                # Main URL routing & media handlers
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
├── portal/                    # Core Academic & College Operations App
│   ├── models.py              # Department, Course, Subject, Timetable,
│   │                          # Attendance, Assignment, Exam, Grade, Notice, Leave
│   ├── views.py               # Portal controllers for Admin, Teacher & Student
│   ├── forms.py               # Django forms for validation & data entry
│   ├── urls.py                # Portal routing endpoints
│   └── management/commands/   # Custom CLI commands
│       └── seed_data.py       # Comprehensive database demo seed script
│
├── templates/                 # UI HTML Templates
│   ├── base.html              # Core layout with sidebar & navigation
│   ├── accounts/              # Login & profile templates
│   └── portal/                # Admin, Teacher, and Student portal views
│
├── static/                    # Static Assets
│   ├── css/style.css          # Design system & responsive styles
│   └── js/                    # UI interactive scripts
│
├── media/                     # Uploaded files (profiles, assignments, submissions)
├── db.sqlite3                 # Local SQLite database
├── manage.py                  # Django management script
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **pip** and **git** installed on your system

---

### Setup Guide

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/college-management-system.git
cd college-management-system
```

#### 2. Create and Activate a Virtual Environment

- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If script execution is disabled, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

- **On Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Populate Sample Demo Data *(Recommended)*
We have included a built-in seeding command that sets up departments, courses, teachers, students, assignments, timetable slots, exams, notices, and test records:
```bash
python manage.py seed_data
```

#### 6. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```url
http://127.0.0.1:8000/
```

---

## 🔑 Demo Accounts & Credentials

If you ran `python manage.py seed_data`, you can instantly log in using any of the pre-configured accounts:

| Role | Username | Password | Notes / Access |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full access to administration portal and Django admin |
| **Faculty / Teacher** | `dr_bikash` | `teacher123` | Head of Dept, CSE instructor (DSA, OS) |
| **Faculty / Teacher** | `prof_sunita` | `teacher123` | Associate Professor, CSE (DBMS) |
| **Faculty / Teacher** | `dr_pradip` | `teacher123` | Assistant Professor, IT (Web Technologies) |
| **Student** | `student_aarav` | `student123` | B.Tech CS, Semester 4 |
| **Student** | `student_sita` | `student123` | B.Tech CS, Semester 4 |
| **Student** | `student_maya` | `student123` | B.Tech IT, Semester 4 |

> 💡 **Tip:** Django Admin interface is accessible at `http://127.0.0.1:8000/admin/`.

---

## ⚡ Custom Management Commands

### `seed_data`
Generates a realistic academic environment with:
- Admin superuser
- Departments: *CSE, IT, Mechanical Engineering*
- Degree Courses: *B.Tech CS, B.Tech IT*
- Instructors with academic designations and qualifications
- Enrolled students with roll numbers and guardians
- Weekly timetable schedules across lecture halls
- Notices, sample assignments, submissions, exams, and attendance logs

To execute:
```bash
python manage.py seed_data
```

---

## ⚙️ Configuration & Production Deployment

When preparing this project for production:

1. **Environment Variables**:
   Move sensitive keys into `.env`:
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'yourdomain.com').split(',')
   ```
2. **Static & Media Files**:
   Run `collectstatic` to gather assets for Nginx/CDN:
   ```bash
   python manage.py collectstatic
   ```
3. **Database**:
   Switch from SQLite to **PostgreSQL** or **MySQL** in `college_system/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'college_db',
           'USER': 'college_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
4. **WSGI Server**:
   Serve using **Gunicorn** or **uWSGI**:
   ```bash
   gunicorn college_system.wsgi:application --bind 0.0.0.0:8000
   ```

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ for educational institutions.</sub>
</div>
