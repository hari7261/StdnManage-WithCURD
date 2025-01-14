import sqlite3
from sqlite3 import Error
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup
DATABASE_NAME = "student_management.db"

# CustomTkinter appearance settings
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Create database connection
def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        print(f"Connected to SQLite database: {DATABASE_NAME}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Create tables
def create_tables(conn):
    """Create all necessary tables in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'student'
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                semester INTEGER NOT NULL,
                subject TEXT NOT NULL,
                marks INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("All tables created or already exist.")
    except Error as e:
        print(f"Error creating tables: {e}")

# Add a new user
def add_user(conn, username, password, name, email, role="student"):
    """Add a new user to the database."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, name, email, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, name, email, role))
        conn.commit()
        print(f"User '{username}' added successfully.")
        return True
    except Error as e:
        print(f"Error adding user: {e}")
        return False

# Authenticate user
def authenticate_user(conn, username, password):
    """Authenticate a user."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error authenticating user: {e}")
        return None

# CustomTkinter App
class StudentManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")
        self.resizable(False, False)

        # Database connection
        self.conn = create_connection()
        if self.conn is not None:
            create_tables(self.conn)
        else:
            messagebox.showerror("Error", "Cannot connect to the database.")
            self.destroy()

        # Current user
        self.current_user = None

        # Show login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display the login screen."""
        self.clear_screen()

        ctk.CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=20)

        ctk.CTkLabel(self, text="Username:").pack()
        self.login_username_entry = ctk.CTkEntry(self, width=300)
        self.login_username_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Password:").pack()
        self.login_password_entry = ctk.CTkEntry(self, width=300, show="*")
        self.login_password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)
        ctk.CTkButton(self, text="Sign Up", command=self.show_signup_screen).pack(pady=10)

    def show_signup_screen(self):
        """Display the signup screen."""
        self.clear_screen()

        ctk.CTkLabel(self, text="Sign Up", font=("Arial", 24)).pack(pady=20)

        ctk.CTkLabel(self, text="Username:").pack()
        self.signup_username_entry = ctk.CTkEntry(self, width=300)
        self.signup_username_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Password:").pack()
        self.signup_password_entry = ctk.CTkEntry(self, width=300, show="*")
        self.signup_password_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Name:").pack()
        self.signup_name_entry = ctk.CTkEntry(self, width=300)
        self.signup_name_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Email:").pack()
        self.signup_email_entry = ctk.CTkEntry(self, width=300)
        self.signup_email_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Role:").pack()
        self.signup_role_entry = ctk.CTkEntry(self, width=300)
        self.signup_role_entry.pack(pady=10)

        ctk.CTkButton(self, text="Sign Up", command=self.signup).pack(pady=20)
        ctk.CTkButton(self, text="Back to Login", command=self.show_login_screen).pack(pady=10)

    def login(self):
        """Handle user login."""
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password are required.")
            return

        user = authenticate_user(self.conn, username, password)
        if user:
            self.current_user = user
            if user[5] == "teacher":
                self.show_teacher_dashboard()
            else:
                self.show_student_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        """Handle user signup."""
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        role = self.signup_role_entry.get()

        if not username or not password or not name or not email or not role:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if add_user(self.conn, username, password, name, email, role):
            messagebox.showinfo("Success", "Account created successfully. Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Failed to create account.")

    def show_teacher_dashboard(self):
        """Display the teacher dashboard."""
        self.clear_screen()

        ctk.CTkLabel(self, text=f"Welcome, {self.current_user[3]} (Teacher)!", font=("Arial", 24)).pack(pady=20)

        # Create tabs
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_view.add("Upload Marks")
        self.tab_view.add("Manage Attendance")
        self.tab_view.add("Assign Assignments")
        self.tab_view.add("Assign Projects")
        self.tab_view.add("View Submissions")
        self.tab_view.add("Notifications")
        self.tab_view.add("Events")

        # Upload Marks Tab
        self.upload_marks_tab = self.tab_view.tab("Upload Marks")
        self.show_upload_marks(self.upload_marks_tab)

        # Manage Attendance Tab
        self.manage_attendance_tab = self.tab_view.tab("Manage Attendance")
        self.show_manage_attendance(self.manage_attendance_tab)

        # Assign Assignments Tab
        self.assign_assignments_tab = self.tab_view.tab("Assign Assignments")
        self.show_assign_assignments(self.assign_assignments_tab)

        # Assign Projects Tab
        self.assign_projects_tab = self.tab_view.tab("Assign Projects")
        self.show_assign_projects(self.assign_projects_tab)

        # View Submissions Tab
        self.view_submissions_tab = self.tab_view.tab("View Submissions")
        self.show_view_submissions(self.view_submissions_tab)

        # Notifications Tab
        self.notifications_tab = self.tab_view.tab("Notifications")
        self.show_notifications(self.notifications_tab)

        # Events Tab
        self.events_tab = self.tab_view.tab("Events")
        self.show_events(self.events_tab)

    def show_student_dashboard(self):
        """Display the student dashboard."""
        self.clear_screen()

        ctk.CTkLabel(self, text=f"Welcome, {self.current_user[3]} (Student)!", font=("Arial", 24)).pack(pady=20)

        # Create tabs
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_view.add("Profile")
        self.tab_view.add("Attendance")
        self.tab_view.add("Marks")
        self.tab_view.add("Assignments")
        self.tab_view.add("Projects")
        self.tab_view.add("Notifications")
        self.tab_view.add("Events")

        # Profile Tab
        self.profile_tab = self.tab_view.tab("Profile")
        self.show_profile(self.profile_tab)

        # Attendance Tab
        self.attendance_tab = self.tab_view.tab("Attendance")
        self.show_attendance(self.attendance_tab)

        # Marks Tab
        self.marks_tab = self.tab_view.tab("Marks")
        self.show_marks(self.marks_tab)

        # Assignments Tab
        self.assignments_tab = self.tab_view.tab("Assignments")
        self.show_assignments(self.assignments_tab)

        # Projects Tab
        self.projects_tab = self.tab_view.tab("Projects")
        self.show_projects(self.projects_tab)

        # Notifications Tab
        self.notifications_tab = self.tab_view.tab("Notifications")
        self.show_notifications(self.notifications_tab)

        # Events Tab
        self.events_tab = self.tab_view.tab("Events")
        self.show_events(self.events_tab)

    def clear_screen(self):
        """Clear the current screen."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_upload_marks(self, tab):
        """Display the upload marks form."""
        ctk.CTkLabel(tab, text="Upload Marks", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(tab, text="Student ID:").pack()
        self.student_id_entry = ctk.CTkEntry(tab, width=300)
        self.student_id_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Semester:").pack()
        self.semester_entry = ctk.CTkEntry(tab, width=300)
        self.semester_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Subject:").pack()
        self.subject_entry = ctk.CTkEntry(tab, width=300)
        self.subject_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Marks:").pack()
        self.marks_entry = ctk.CTkEntry(tab, width=300)
        self.marks_entry.pack(pady=10)

        ctk.CTkButton(tab, text="Upload Marks", command=self.upload_marks).pack(pady=20)

    def upload_marks(self):
        """Handle uploading marks."""
        student_id = self.student_id_entry.get()
        semester = self.semester_entry.get()
        subject = self.subject_entry.get()
        marks = self.marks_entry.get()

        if not student_id or not semester or not subject or not marks:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO marks (user_id, semester, subject, marks)
            VALUES (?, ?, ?, ?)
        ''', (student_id, semester, subject, marks))
        self.conn.commit()
        messagebox.showinfo("Success", "Marks uploaded successfully.")

    def show_manage_attendance(self, tab):
        """Display the manage attendance form."""
        ctk.CTkLabel(tab, text="Manage Attendance", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(tab, text="Student ID:").pack()
        self.attendance_student_id_entry = ctk.CTkEntry(tab, width=300)
        self.attendance_student_id_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Date (YYYY-MM-DD):").pack()
        self.attendance_date_entry = ctk.CTkEntry(tab, width=300)
        self.attendance_date_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Status (Present/Absent):").pack()
        self.attendance_status_entry = ctk.CTkEntry(tab, width=300)
        self.attendance_status_entry.pack(pady=10)

        ctk.CTkButton(tab, text="Submit Attendance", command=self.submit_attendance).pack(pady=20)

    def submit_attendance(self):
        """Handle submitting attendance."""
        student_id = self.attendance_student_id_entry.get()
        date = self.attendance_date_entry.get()
        status = self.attendance_status_entry.get()

        if not student_id or not date or not status:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (user_id, date, status)
            VALUES (?, ?, ?)
        ''', (student_id, date, status))
        self.conn.commit()
        messagebox.showinfo("Success", "Attendance submitted successfully.")

    def show_assign_assignments(self, tab):
        """Display the assign assignments form."""
        ctk.CTkLabel(tab, text="Assign Assignments", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(tab, text="Student ID:").pack()
        self.assignment_student_id_entry = ctk.CTkEntry(tab, width=300)
        self.assignment_student_id_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Title:").pack()
        self.assignment_title_entry = ctk.CTkEntry(tab, width=300)
        self.assignment_title_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Description:").pack()
        self.assignment_description_entry = ctk.CTkEntry(tab, width=300)
        self.assignment_description_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Deadline (YYYY-MM-DD):").pack()
        self.assignment_deadline_entry = ctk.CTkEntry(tab, width=300)
        self.assignment_deadline_entry.pack(pady=10)

        ctk.CTkButton(tab, text="Assign Assignment", command=self.assign_assignment).pack(pady=20)

    def assign_assignment(self):
        """Handle assigning assignments."""
        student_id = self.assignment_student_id_entry.get()
        title = self.assignment_title_entry.get()
        description = self.assignment_description_entry.get()
        deadline = self.assignment_deadline_entry.get()

        if not student_id or not title or not description or not deadline:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO assignments (user_id, title, description, deadline)
            VALUES (?, ?, ?, ?)
        ''', (student_id, title, description, deadline))
        self.conn.commit()
        messagebox.showinfo("Success", "Assignment assigned successfully.")

    def show_assign_projects(self, tab):
        """Display the assign projects form."""
        ctk.CTkLabel(tab, text="Assign Projects", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(tab, text="Student ID:").pack()
        self.project_student_id_entry = ctk.CTkEntry(tab, width=300)
        self.project_student_id_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Title:").pack()
        self.project_title_entry = ctk.CTkEntry(tab, width=300)
        self.project_title_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Description:").pack()
        self.project_description_entry = ctk.CTkEntry(tab, width=300)
        self.project_description_entry.pack(pady=10)

        ctk.CTkLabel(tab, text="Deadline (YYYY-MM-DD):").pack()
        self.project_deadline_entry = ctk.CTkEntry(tab, width=300)
        self.project_deadline_entry.pack(pady=10)

        ctk.CTkButton(tab, text="Assign Project", command=self.assign_project).pack(pady=20)

    def assign_project(self):
        """Handle assigning projects."""
        student_id = self.project_student_id_entry.get()
        title = self.project_title_entry.get()
        description = self.project_description_entry.get()
        deadline = self.project_deadline_entry.get()

        if not student_id or not title or not description or not deadline:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO projects (user_id, title, description, deadline)
            VALUES (?, ?, ?, ?)
        ''', (student_id, title, description, deadline))
        self.conn.commit()
        messagebox.showinfo("Success", "Project assigned successfully.")

    def show_view_submissions(self, tab):
        """Display student submissions."""
        ctk.CTkLabel(tab, text="View Submissions", font=("Arial", 20)).pack(pady=10)

        # Fetch assignments
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id, title, description, deadline, status FROM assignments
        ''')
        assignments = cursor.fetchall()

        if not assignments:
            ctk.CTkLabel(tab, text="No assignments found.").pack()
        else:
            for assignment in assignments:
                ctk.CTkLabel(tab, text=f"Student ID: {assignment[0]}, Title: {assignment[1]}, Deadline: {assignment[3]}, Status: {assignment[4]}").pack()

        # Fetch projects
        cursor.execute('''
            SELECT user_id, title, description, deadline, status FROM projects
        ''')
        projects = cursor.fetchall()

        if not projects:
            ctk.CTkLabel(tab, text="No projects found.").pack()
        else:
            for project in projects:
                ctk.CTkLabel(tab, text=f"Student ID: {project[0]}, Title: {project[1]}, Deadline: {project[3]}, Status: {project[4]}").pack()

    def show_notifications(self, tab):
        """Display notifications."""
        ctk.CTkLabel(tab, text="Notifications", font=("Arial", 20)).pack(pady=10)

        # Fetch notifications
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT message, date FROM notifications
            WHERE user_id = ?
        ''', (self.current_user[0],))
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No notifications found.").pack()
        else:
            for record in records:
                ctk.CTkLabel(tab, text=f"Date: {record[1]}, Message: {record[0]}").pack()

    def show_events(self, tab):
        """Display events."""
        ctk.CTkLabel(tab, text="Events", font=("Arial", 20)).pack(pady=10)

        # Fetch events
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT title, description, date FROM events
        ''')
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No events found.").pack()
        else:
            for record in records:
                ctk.CTkLabel(tab, text=f"Date: {record[2]}, Title: {record[0]}, Description: {record[1]}").pack()

    def show_profile(self, tab):
        """Display user profile."""
        ctk.CTkLabel(tab, text="Profile", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(tab, text=f"Name: {self.current_user[3]}").pack()
        ctk.CTkLabel(tab, text=f"Email: {self.current_user[4]}").pack()
        ctk.CTkLabel(tab, text=f"Role: {self.current_user[5]}").pack()

    def show_attendance(self, tab):
        """Display attendance as a pie chart."""
        ctk.CTkLabel(tab, text="Attendance", font=("Arial", 20)).pack(pady=10)

        # Fetch attendance records
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT status FROM attendance
            WHERE user_id = ?
        ''', (self.current_user[0],))
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No attendance records found.").pack()
        else:
            present = records.count(("Present",))
            absent = records.count(("Absent",))

            # Create pie chart
            fig, ax = plt.subplots()
            ax.pie([present, absent], labels=["Present", "Absent"], autopct="%1.1f%%", startangle=90)
            ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.

            # Embed pie chart in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def show_marks(self, tab):
        """Display marks for each semester."""
        ctk.CTkLabel(tab, text="Marks", font=("Arial", 20)).pack(pady=10)

        # Fetch marks records
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT semester, subject, marks FROM marks
            WHERE user_id = ?
        ''', (self.current_user[0],))
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No marks records found.").pack()
        else:
            for record in records:
                ctk.CTkLabel(tab, text=f"Semester: {record[0]}, Subject: {record[1]}, Marks: {record[2]}").pack()

    def show_assignments(self, tab):
        """Display assignments."""
        ctk.CTkLabel(tab, text="Assignments", font=("Arial", 20)).pack(pady=10)

        # Fetch assignments
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT title, description, deadline, status FROM assignments
            WHERE user_id = ?
        ''', (self.current_user[0],))
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No assignments found.").pack()
        else:
            for record in records:
                ctk.CTkLabel(tab, text=f"Title: {record[0]}, Deadline: {record[2]}, Status: {record[3]}").pack()

    def show_projects(self, tab):
        """Display projects."""
        ctk.CTkLabel(tab, text="Projects", font=("Arial", 20)).pack(pady=10)

        # Fetch projects
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT title, description, deadline, status FROM projects
            WHERE user_id = ?
        ''', (self.current_user[0],))
        records = cursor.fetchall()

        if not records:
            ctk.CTkLabel(tab, text="No projects found.").pack()
        else:
            for record in records:
                ctk.CTkLabel(tab, text=f"Title: {record[0]}, Deadline: {record[2]}, Status: {record[3]}").pack()

# Run the application
if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()