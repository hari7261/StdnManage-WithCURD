# Student Management System (SMS)

The **Student Management System (SMS)** is a comprehensive application designed to manage student and teacher activities in an educational institution. It provides separate environments for **students** and **teachers**, allowing them to interact with the system based on their roles. The system is built using **Python**, **SQLite** for database management, and **CustomTkinter** for the graphical user interface (GUI).

---

## Features

### **For Teachers**
1. **Upload Marks**: Teachers can upload marks for students for each semester.
2. **Manage Attendance**: Teachers can mark attendance for students (Present/Absent).
3. **Assign Assignments**: Teachers can assign assignments to students with deadlines.
4. **Assign Projects**: Teachers can assign projects to students with deadlines.
5. **View Submissions**: Teachers can view student submissions for assignments and projects.
6. **Notifications**: Teachers can view important notifications.
7. **Events**: Teachers can view upcoming events.

### **For Students**
1. **Profile Management**: Students can view their profile details.
2. **Attendance**: Students can view their attendance records as a **pie chart**.
3. **Marks**: Students can view their marks for each semester.
4. **Assignments**: Students can view and submit assignments.
5. **Projects**: Students can view and submit projects.
6. **Notifications**: Students can view important notifications.
7. **Events**: Students can view upcoming events.

---

## Technologies Used

- **Python**: The core programming language used for development.
- **SQLite**: A lightweight database used to store all data.
- **CustomTkinter**: A modern GUI library for creating the user interface.
- **Matplotlib**: Used to generate pie charts for attendance visualization.

---

## Database Schema

The SQLite database contains the following tables:

1. **users**:
   - Stores user login credentials and profiles.
   - Columns: `id`, `username`, `password`, `name`, `email`, `role`.

2. **attendance**:
   - Stores attendance records for students.
   - Columns: `id`, `user_id`, `date`, `status`.

3. **marks**:
   - Stores marks for each semester.
   - Columns: `id`, `user_id`, `semester`, `subject`, `marks`.

4. **assignments**:
   - Stores assignment details.
   - Columns: `id`, `user_id`, `title`, `description`, `deadline`, `status`.

5. **projects**:
   - Stores project details.
   - Columns: `id`, `user_id`, `title`, `description`, `deadline`, `status`.

6. **notifications**:
   - Stores notifications for users.
   - Columns: `id`, `user_id`, `message`, `date`.

7. **events**:
   - Stores upcoming events.
   - Columns: `id`, `title`, `description`, `date`.

---

## How to Run the Application

### Prerequisites
1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install the required libraries using pip:
   ```bash
   pip install customtkinter matplotlib
   ```

### Steps to Run
1. Download or clone the repository.
2. Navigate to the project directory.
3. Run the application:
   ```bash
   python student_management.py
   ```
4. Use the GUI to interact with the system.

---

## User Guide

### **Login/Signup**
1. **Login**:
   - Enter your username and password to log in.
   - Teachers and students have separate dashboards based on their roles.

2. **Signup**:
   - New users can sign up by providing a username, password, name, email, and role (student/teacher).

### **Teacher Dashboard**
1. **Upload Marks**:
   - Enter the student ID, semester, subject, and marks to upload marks.

2. **Manage Attendance**:
   - Enter the student ID, date, and status (Present/Absent) to mark attendance.

3. **Assign Assignments**:
   - Enter the student ID, title, description, and deadline to assign an assignment.

4. **Assign Projects**:
   - Enter the student ID, title, description, and deadline to assign a project.

5. **View Submissions**:
   - View all assignments and projects submitted by students.

6. **Notifications**:
   - View important notifications.

7. **Events**:
   - View upcoming events.

### **Student Dashboard**
1. **Profile**:
   - View your profile details (name, email, role).

2. **Attendance**:
   - View your attendance records as a pie chart.

3. **Marks**:
   - View your marks for each semester.

4. **Assignments**:
   - View and submit assignments.

5. **Projects**:
   - View and submit projects.

6. **Notifications**:
   - View important notifications.

7. **Events**:
   - View upcoming events.

---

## Screenshots

### Login Screen
![Login Screen](https://via.placeholder.com/600x400?text=Login+Screen)

### Teacher Dashboard
![Teacher Dashboard](https://via.placeholder.com/600x400?text=Teacher+Dashboard)

### Student Dashboard
![Student Dashboard](https://via.placeholder.com/600x400?text=Student+Dashboard)

### Attendance Pie Chart
![Attendance Pie Chart](https://via.placeholder.com/600x400?text=Attendance+Pie+Chart)

---

## Code Structure

The code is modular and organized into the following sections:
1. **Database Setup**:
   - Functions to create a database connection and tables.
2. **CRUD Operations**:
   - Functions to add, update, delete, and fetch data from the database.
3. **GUI**:
   - CustomTkinter-based GUI for the application.
4. **Teacher Environment**:
   - Functions and GUI components for teacher-specific features.
5. **Student Environment**:
   - Functions and GUI components for student-specific features.



## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the **Student Management System**! We hope it simplifies your educational management tasks.