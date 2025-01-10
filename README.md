# CSE370_Project
An Edtech web application for cse370(database systems) course.

## Screenshots
![BeFunky-collage](https://github.com/user-attachments/assets/62c322fa-e175-4f8d-a345-3e460a881424)
## Features
### Core Features
- **Authentication System**:
  - User registration, login, and logout
  - role-based access for Students, Teachers, and Admins.
- **Course Management**:
  - Create, update, and delete courses.
  - Add text content, video content, and a thumbnail to each course.
- **Dynamic Dashboards**:
  - **Student Dashboard**: View enrolled courses and progress.
  - **Teacher Dashboard**: Manage created courses and view engagement metrics.
  - **Admin Dashboard**: Oversee all courses, users, and content.
- **Responsive Design**: Fully responsive UI built with Bootstrap for an optimal user experience on all devices.

### Pages Overview
- **Login**
- **Register**
- **Homepage**:
  - navbar, banner, mission and vision, featured Courses, Testimonials, footer
- **Course Detail Page**:
  - course description, text, and video content, option to enroll (for Students) or edit (for Teachers).
- **All Course**
- **About Us**
- **Student Dashboard**:
  - Sidebar list (for navigations)
  - (sidebar:Profile) edit email, profile pic, first-name, last-name, delete account btn
  - (sidebar:Course) course progress, overall progress, badge
  - (sidebar:Dashboard) course progress, overall progress, badge
- **Teacher Dashboard**:
  - Sidebar list (for navigations)
  - (sidebar:Profile) edit email, profile pic, first-name, last-name, delete account btn
  - (sidebar:Create) Course creation form
  - (sidebar:Dashboard) course enrollment status, overal enrollment status, created courses list (can view, delete)
- **Admin Dashboard**:
  - (sidebar:User) manage user(delete, add, modify, set role, see login history),
  - (sidebar:Course) manage Courses(delete, add, modify),
  - (sidebar:Enrollment) manage Enrollment(view all enrollment, create, delete),
  - (sidebar: Static) manage Static contensts of home and about (can edit contents),

### Technologies Used
- Backend: `Django`
- Frontend: `HTML`, `CSS`, `Bootstrap5`
- Database: `MySQL`
- Authentication: Django's built-in authentication framework

---

## Installation and Setup
1. Clone the repository:
  ```bash
  git clone git@github.com:Naahian/CSE370_Project.git
  cd CSE370_Project
  ```
2. Install django:
  ```bash
  pip install django
  ```
3. Set up the database, Run migrations:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
4. Run the development server:
```bash
python manage.py runserver
```
5. Access the application at http://127.0.0.1:8000/.
