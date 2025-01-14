from app.models import User, Student, Instructor, Course
from app.utils import verify_password
from app.database import get_db_cursor


class AuthenticationService:
    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and verify_password(password, user[2]):  # User schema: (id, username, hashed_password, email, role)
            print(f"Welcome {user[1]}!")
            return user
        else:
            print("Invalid username or password.")
            return None


class SessionManager:
    current_user = None

    @staticmethod
    def login_user(user):
        SessionManager.current_user = user

    @staticmethod
    def logout_user():
        SessionManager.current_user = None

    @staticmethod
    def is_authenticated():
        return SessionManager.current_user is not None

    @staticmethod
    def has_role(role):
        return SessionManager.current_user and SessionManager.current_user[4] == role


class AdminService:
    @staticmethod
    def manage_students():
        print("\n--- Manage Students ---")
        print("1. Add Student\n2. Update Student\n3. Delete Student\n4. View Students")
        choice = input("Choose an option: ")

        if choice == "1":
            StudentService.add_student()
        elif choice == "2":
            StudentService.update_student()
        elif choice == "3":
            StudentService.delete_student()
        elif choice == "4":
            StudentService.view_all_students()
        else:
            print("Invalid choice.")

    @staticmethod
    def manage_courses():
        print("\n--- Manage Courses ---")
        print("1. Add Course\n2. Update Course\n3. Delete Course\n4. View Courses")
        choice = input("Choose an option: ")

        if choice == "1":
            CourseService.add_course()
        elif choice == "2":
            CourseService.update_course()
        elif choice == "3":
            CourseService.delete_course()
        elif choice == "4":
            CourseService.view_all_courses()
        else:
            print("Invalid choice.")

    @staticmethod
    def view_reports():
        print("\n--- Generate Reports ---")
        print("1. Student Enrollment Statistics\n2. Course Enrollment Statistics")
        choice = input("Choose an option: ")

        if choice == "1":
            ReportingService.student_enrollment_report()
        elif choice == "2":
            ReportingService.course_enrollment_report()
        else:
            print("Invalid choice.")


class StudentService:
    @staticmethod
    def add_student():
        print("\n--- Add New Student ---")
        try:
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")
            user = User(username, password, email, "student")
            user.create()

            student_id = user.cursor.lastrowid
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
            phone = input("Phone Number (optional): ")
            admission_date = input("Admission Date (YYYY-MM-DD): ")
            major = input("Major: ")
            status = "active"

            student = Student(student_id, first_name, last_name, date_of_birth, admission_date, major, status)
            student.create()
            print("Student added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def update_student():
        print("\n--- Update Student Details ---")
        student_id = input("Enter Student ID: ")

        try:
            cursor = get_db_cursor()
            cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()

            if not student:
                print("Student not found.")
                return

            print("Leave field blank to keep current value.")
            first_name = input(f"First Name [{student[2]}]: ") or student[2]
            last_name = input(f"Last Name [{student[3]}]: ") or student[3]
            phone = input(f"Phone [{student[5]}]: ") or student[5]
            major = input(f"Major [{student[7]}]: ") or student[7]
            status = input(f"Status [{student[8]}]: ") or student[8]

            cursor.execute("""
                UPDATE Students
                SET first_name = ?, last_name = ?, phone = ?, major = ?, status = ?
                WHERE student_id = ?
            """, (first_name, last_name, phone, major, status, student_id))
            print("Student updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def delete_student():
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID: ")

        try:
            cursor = get_db_cursor()
            cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
            print("Student deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_all_students():
        print("\n--- All Students ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("SELECT student_id, first_name, last_name, major, status FROM Students")
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Major: {row[3]}, Status: {row[4]}")
            else:
                print("No students found.")
        except Exception as e:
            print(f"Error: {e}")


class InstructorService:
    @staticmethod
    def view_assigned_courses():
        print("\n--- Assigned Courses ---")
        try:
            instructor_id = SessionManager.current_user[0]
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT course_id, course_code, title, credits
                FROM Courses
                WHERE instructor_id = ?
            """, (instructor_id,))
            courses = cursor.fetchall()

            if courses:
                for course in courses:
                    print(f"Course ID: {course[0]}, Code: {course[1]}, Title: {course[2]}, Credits: {course[3]}")
            else:
                print("No assigned courses.")
        except Exception as e:
            print(f"Error: {e}")


class ReportingService:
    @staticmethod
    def student_enrollment_report():
        print("\n--- Student Enrollment Report ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT Students.major, COUNT(Enrollments.student_id)
                FROM Enrollments
                INNER JOIN Students ON Enrollments.student_id = Students.student_id
                GROUP BY Students.major
            """)
            rows = cursor.fetchall()

            for row in rows:
                print(f"Major: {row[0]}, Enrollments: {row[1]}")
        except Exception as e:
            print(f"Error: {e}")


class CourseService:
    @staticmethod
    def add_course():
        print("\n--- Add New Course ---")
        course_code = input("Course Code: ")
        title = input("Course Title: ")
        credits = input("Credits: ")
        max_enrollment = input("Max Enrollment: ")
        prerequisites = input("Prerequisites: ")
        instructor_id = input("Instructor ID: ")

        status = "active"

        try:
            course = Course(course_code, title, credits, max_enrollment, prerequisites, instructor_id, status)
            course.create()
            print("Course added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def update_course():
        print("\n--- Update Course Details ---")
        course_id = input("Enter Course ID: ")

        try:
            cursor = get_db_cursor()
            cursor.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,))
            course = cursor.fetchone()

            if not course:
                print("Course not found.")
                return

            print("Leave field blank to keep current value.")
            title = input(f"Title [{course[2]}]: ") or course[2]
            credits = input(f"Credits [{course[3]}]: ") or course[3]
            prerequisites = input(f"Prerequisites [{course[4]}]: ") or course[4]

            cursor.execute("""
                UPDATE Courses
                SET title = ?, credits = ?, prerequisites = ?
                WHERE course_id = ?
            """, (title, credits, prerequisites, course_id))
            print("Course updated successfully.")
        except Exception as e:
            print(f"Error: {e}")


class SessionManager:
    current_user = None

    @staticmethod
    def login_user(user):
        SessionManager.current_user = user

    @staticmethod
    def logout_user():
        SessionManager.current_user = None

    @staticmethod
    def is_authenticated():
        return SessionManager.current_user is not None

    @staticmethod
    def has_role(role):
        return SessionManager.current_user and SessionManager.current_user[4] == role
