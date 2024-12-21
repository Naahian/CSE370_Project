# CSE370_Project
An Edtech web application for cse370(database systems) course.

## Screenshots
(screenshot image)  

## Features
### Core Features
- **Authentication System**: User registration, login, and logout functionality with role-based access for Students, Teachers, and Admins.
- **Course Management**:
  - Create, update, and delete courses.
  - Add text content, video content, and a thumbnail to each course.
- **Dynamic Dashboards**:
  - **Student Dashboard**: View enrolled courses and progress.
  - **Teacher Dashboard**: Manage created courses and view engagement metrics.
  - **Admin Dashboard**: Oversee all courses, users, and content.
- **Responsive Design**: Fully responsive UI built with Bootstrap for an optimal user experience on all devices.

### Pages Overview
- **Homepage**: navbar, banner, mission and vision, featured Courses, Testimonials, footer
- **Course Detail Page**: course description, text, and video content, option to enroll (for Students) or edit (for Teachers).
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
  - (default django admin dashboard) Manage users, courses, and overall application settings.

### Technologies Used
- Backend: Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQL
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
  pip install -r django
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

## Contributing
Contributions are welcome! To contribute:
- Fork this repository.
- Create a feature branch: `git checkout -b feature-name`
- Commit your changes: `git commit -m "Add some feature"`
- Push to the branch: `git push origin feature-name`
- Open a pull request.
