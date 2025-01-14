from app.models import User, Student, Instructor, Course, Grade
from app.utils import verify_password, hash_password
from app.database import get_db_cursor
from app.errors import SystemErrors

# Decorator for role-based access control
def role_required(required_role):
    if not SessionManager.is_authenticated():
        print("Access denied. User not authenticated.")
        return None
    if SessionManager.current_user[4] != required_role:
        print(f"Access denied. {required_role} role required.")
        return None
           

class AuthenticationService:
    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and verify_password(password, user[2]):  # User schema: (id, username, hashed_password, email, role)
            SessionManager.login_user(user)
            print(f"Welcome {user[1]}!")
            return user
        else:
            print("Invalid username or password.")
            return None

    @staticmethod
    def reset_password(username, new_password):
        user = User.find_by_username(username)
        if not user:
            print("User not found.")
            return False

        hashed_password = hash_password(new_password)
        User.update_password(username, hashed_password)
        print("Password reset successfully.")
        return True

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
    @role_required("admin")
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
    @role_required("admin")
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

class StudentService:
    @staticmethod
    @role_required("admin")
    def add_student():
        print("\n--- Add New Student ---")
        try:
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")
            user = User(username, hash_password(password), email, "student")
            user.create()

            student_id = user.cursor.lastrowid
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
            admission_date = input("Admission Date (YYYY-MM-DD): ")
            major = input("Major: ")
            status = "active"

            student = Student(student_id, first_name, last_name, date_of_birth, admission_date, major, status)
            student.create()
            print("Student added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    @role_required("admin")
    def update_student():
        print("\n--- Update Student Details ---")
        student_id = input("Enter Student ID: ")

        student = Student.find_by_id(student_id)
        if not student:
            print("Student not found.")
            return

        print("Leave field blank to keep current value.")
        first_name = input(f"First Name [{student.first_name}]: ") or student.first_name
        last_name = input(f"Last Name [{student.last_name}]: ") or student.last_name
        major = input(f"Major [{student.major}]: ") or student.major
        status = input(f"Status [{student.status}]: ") or student.status

        try:
            student.update(first_name=first_name, last_name=last_name, major=major, status=status)
            print("Student updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    @role_required("admin")
    def delete_student():
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID: ")

        try:
            Student.delete(student_id)
            print("Student deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_all_students():
        print("\n--- All Students ---")
        try:
            students = Student.find_all()
            if students:
                for student in students:
                    print(f"ID: {student[0]}, Name: {student[1]} {student[2]}, Major: {student[3]}, Status: {student[4]}")
            else:
                print("No students found.")
        except Exception as e:
            print(f"Error: {e}")

class CourseService:
    @staticmethod
    @role_required("admin")
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
    @role_required("admin")
    def update_course():
        print("\n--- Update Course Details ---")
        course_id = input("Enter Course ID: ")

        course = Course.find_by_id(course_id)
        if not course:
            print("Course not found.")
            return

        print("Leave field blank to keep current value.")
        title = input(f"Title [{course.title}]: ") or course.title
        credits = input(f"Credits [{course.credits}]: ") or course.credits
        prerequisites = input(f"Prerequisites [{course.prerequisites}]: ") or course.prerequisites

        try:
            course.update(title=title, credits=credits, prerequisites=prerequisites)
            print("Course updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

class InstructorService:
    @staticmethod
    def view_assigned_courses(instructor_id):
        print("\n--- Assigned Courses ---")
        try:
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

    @staticmethod
    def manage_grades(course_id):
        print("\n--- Manage Grades ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT student_id, first_name, last_name, grade
                FROM Enrollments
                INNER JOIN Students ON Enrollments.student_id = Students.student_id
                WHERE course_id = ?
            """, (course_id,))
            students = cursor.fetchall()

            if not students:
                print("No students enrolled in this course.")
                return

            for student in students:
                print(f"Student ID: {student[0]}, Name: {student[1]} {student[2]}, Current Grade: {student[3] or 'N/A'}")
                grade = input("Enter grade (or leave blank to skip): ")

                if grade and grade not in GRADE_POINTS:
                    print(SystemErrors.INVALID_GRADE['message'])
                    continue

                if grade:
                    cursor.execute("""
                        UPDATE Enrollments SET grade = ? WHERE student_id = ? AND course_id = ?
                    """, (grade, student[0], course_id))
                    print("Grade updated successfully.")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_course_statistics(course_id):
        print("\n--- Course Statistics ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT grade, COUNT(*)
                FROM Enrollments
                WHERE course_id = ? AND grade IS NOT NULL
                GROUP BY grade
            """, (course_id,))
            stats = cursor.fetchall()

            if stats:
                print("Grade Distribution:")
                for grade, count in stats:
                    print(f"Grade: {grade}, Count: {count}")
            else:
                print("No grades assigned yet.")
        except Exception as e:
            print(f"Error: {e}")

GRADE_POINTS = {
    'A+': {'points': 5.0, 'range': '80-100', 'class': 'First Class'},
    'A':  {'points': 4.75, 'range': '75-79', 'class': 'First Class'},
    'A-': {'points': 4.5, 'range': '70-74', 'class': 'First Class'},
    'B+': {'points': 4.0, 'range': '65-69', 'class': 'Upper Second'},
    'B':  {'points': 3.75, 'range': '63-64', 'class': 'Upper Second'},
    'B-': {'points': 3.5, 'range': '60-62', 'class': 'Upper Second'},
    'C+': {'points': 3.0, 'range': '55-59', 'class': 'Lower Second'},
    'C':  {'points': 2.75, 'range': '53-54', 'class': 'Lower Second'},
    'C-': {'points': 2.5, 'range': '50-52', 'class': 'Lower Second'},
    'D+': {'points': 2.0, 'range': '45-49', 'class': 'Third'},
    'D':  {'points': 1.5, 'range': '43-44', 'class': 'Third'},
    'D-': {'points': 1.0, 'range': '40-42', 'class': 'Third'},
    'F':  {'points': 0.0, 'range': '0-39', 'class': 'Fail'}
}

class ReportingService:
    @staticmethod
    def course_performance_report(course_id):
        print("\n--- Course Performance Report ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT Students.first_name, Students.last_name, Enrollments.grade
                FROM Enrollments
                INNER JOIN Students ON Enrollments.student_id = Students.student_id
                WHERE course_id = ?
            """, (course_id,))
            rows = cursor.fetchall()

            if rows:
                print("Student Performance:")
                for row in rows:
                    print(f"Name: {row[0]} {row[1]}, Grade: {row[2]}")
            else:
                print("No data available for this course.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def grade_distribution_report():
        print("\n--- Grade Distribution Report ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT grade, COUNT(*)
                FROM Enrollments
                WHERE grade IS NOT NULL
                GROUP BY grade
            """)
            rows = cursor.fetchall()

            if rows:
                print("Grade Distribution:")
                for row in rows:
                    print(f"Grade: {row[0]}, Count: {row[1]}")
            else:
                print("No grades assigned yet.")
        except Exception as e:
            print(f"Error: {e}")
