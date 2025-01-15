from app.models import User, Student, Grade, Enrollment
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
    def register_user(username, password, role="student"):
        """
        Registers a new user in the database.
        """
        if User.find_by_username(username):
            print("Error: Username already exists.")
            return False

        hashed_password = hash_password(password)
  
        user = User(username, hashed_password, role)
        user.create()
        return True

    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and verify_password(password, user[2]): 
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
    def manage_reg_nos():
        print("\n--- Manage reg_nos ---")
        print("1. Add reg_no\n2. Update reg_no\n3. Delete reg_no\n4. View reg_nos")
        choice = input("Choose an option: ")

        if choice == "1":
            reg_noService.add_reg_no()
        elif choice == "2":
            reg_noService.update_reg_no()
        elif choice == "3":
            reg_noService.delete_reg_no()
        elif choice == "4":
            reg_noService.view_all_reg_nos()
        else:
            print("Invalid choice.")
    
    @staticmethod
    def view_reports():
        print("\n--- View Reports ---")
        print("1. View Student Transcripts")
        print("2. View reg_no List")
        print("3. View Enrollment Statistics")
        print("4. Go Back")

        choice = input("Choose an option: ")

        if choice == "1":
            AdminService.view_student_transcripts()
        elif choice == "2":
            AdminService.view_reg_no_list()
        elif choice == "3":
            AdminService.view_enrollment_statistics()
        elif choice == "4":
            print("Returning to Admin Menu...")
        else:
            print("Invalid choice. Please try again.")
    
    @staticmethod
    def view_student_transcripts():
        print("\n--- Student Transcripts ---")
        reg_no = input("Enter Student Registration Number: ")

        cursor = get_db_cursor()[0]
        cursor.execute("""
            SELECT reg_nos.title, Grades.grade_value, Grades.numeric_grade
            FROM Grades
            INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.enrollment_id
            INNER JOIN reg_nos ON Enrollments.reg_no_id = reg_nos.reg_no_id
            INNER JOIN Students ON Enrollments.student_id = Students.student_id
            WHERE Students.reg_no = ?
        """, (reg_no,))
        transcript = cursor.fetchall()

        if transcript:
            print(f"\nTranscript for Student {reg_no}:")
            for reg_no_title, grade_value, numeric_grade in transcript:
                print(f"reg_no: {reg_no_title}, Grade: {grade_value}, Numeric Grade: {numeric_grade}")
        else:
            print("No transcript found for the given registration number.")
    
    @staticmethod
    def view_reg_no_list():
        print("\n--- reg_no List ---")

        cursor = get_db_cursor()[0]
        cursor.execute("SELECT reg_no_code, title FROM reg_nos WHERE status = 'active'")
        reg_nos = cursor.fetchall()

        if reg_nos:
            print("\nActive reg_nos:")
            for reg_no_code, title in reg_nos:
                print(f"reg_no Code: {reg_no_code}, reg_no Title: {title}")
        else:
            print("No active reg_nos found.")

    @staticmethod
    def view_enrollment_statistics():
        print("\n--- Enrollment Statistics ---")

        cursor = get_db_cursor()[0]
        cursor.execute("""
            SELECT reg_nos.title, COUNT(Enrollments.student_id) 
            FROM Enrollments
            INNER JOIN reg_nos ON Enrollments.reg_no_id = reg_nos.reg_no_id
            WHERE reg_nos.status = 'active'
            GROUP BY reg_nos.title
        """)
        stats = cursor.fetchall()

        if stats:
            print("\nEnrollment Statistics:")
            for reg_no_title, enrollment_count in stats:
                print(f"reg_no: {reg_no_title}, Enrolled Students: {enrollment_count}")
        else:
            print("No enrollment statistics available.")



class StudentService:
    @staticmethod
    def add_student():
        print("\n--- Add New Student ---")
        try:
            username = input("Username: ")
            password = input("Password: ")
            user = User(username, hash_password(password), "student")
            user.create()

            user_id = user.cursor.lastrowid
            reg_no = input("Registration Number: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            admission_date = input("Admission Date (YYYY-MM-DD): ")
            major = input("Major: ")
            status = "active"

            student = Student(user_id, reg_no, first_name, last_name, admission_date, major, status)
            student.create()
            print("Student added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_all_students():
        print("\n--- All Students ---")
        try:
            students = Student.find_all()
            if students:
                for student in students:
                    print(f"Reg No: {student[2]}, Name: {student[3]} {student[4]}, Major: {student[6]}, Status: {student[7]}")
            else:
                print("No students found.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def update_student():
        print("\n--- Update Student Details ---")
        reg_no = input("Enter Registration Number: ")

        # Retrieve the student by reg_no
        student_data = Student.find_by_reg_no(reg_no)
        if not student_data:
            print("Student not found.")
            return

        # Unpack the student data
        student_id, user_id, reg_no, first_name, last_name, admission_date, major, status = student_data

        print("Leave field blank to keep current value.")
        first_name = input(f"First Name [{first_name}]: ") or first_name
        last_name = input(f"Last Name [{last_name}]: ") or last_name
        major = input(f"Major [{major}]: ") or major
        status = input(f"Status [{status}]: ") or status

        try:
            # Create student instance
            student_instance = Student(student_id, first_name, last_name, major, status)
            # Call the update method on the student instance
            student_instance.update(first_name, last_name, major, status)
            print("Student updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    
    @staticmethod
    def delete_student():
        print("\n--- Delete Student ---")
        reg_no = input("Enter Registration Number: ")

        try:
            # Retrieve the student to check if it exists before deletion
            student_data = Student.find_by_reg_no(reg_no)
            if not student_data:
                print("Student not found.")
                return
            
            # Proceed to delete the student by reg_no
            Student.delete(reg_no)
            print("Student deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
    
class InstructorService:
    @staticmethod
    def view_assigned_reg_nos():
        if not SessionManager.is_authenticated():
            print("Please log in to view assigned reg_nos.")
            return
        
        instructor_id = SessionManager.current_user[0]  
        
        print(f"\n--- reg_nos Assigned to Instructor {instructor_id} ---")

        cursor = get_db_cursor()[0]
        cursor.execute("""
            SELECT reg_nos.reg_no_code, reg_nos.title, reg_nos.credits, reg_nos.max_enrollment
            FROM reg_nos
            WHERE reg_nos.instructor_id = ?
        """, (instructor_id,))
        
        reg_nos = cursor.fetchall()

        if reg_nos:
            print(f"\n{'reg_no Code':<20}{'Title':<40}{'Credits':<10}{'Max Enrollment':<20}")
            print("-" * 90)
            for reg_no in reg_nos:
                reg_no_code, title, credits, max_enrollment = reg_no
                print(f"{reg_no_code:<20}{title:<40}{credits:<10}{max_enrollment:<20}")
        else:
            print("No reg_nos assigned.")


    @staticmethod
    def manage_grades(reg_no_id):
        print("\n--- Manage Grades ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT student_id, first_name, last_name, grade
                FROM Enrollments
                INNER JOIN Students ON Enrollments.student_id = Students.student_id
                WHERE reg_no_id = ?
            """, (reg_no_id,))
            students = cursor.fetchall()

            if not students:
                print("No students enrolled in this reg_no.")
                return

            for student in students:
                print(f"Student ID: {student[0]}, Name: {student[1]} {student[2]}, Current Grade: {student[3] or 'N/A'}")
                grade = input("Enter grade (or leave blank to skip): ")

                if grade and grade not in GRADE_POINTS:
                    print(SystemErrors.INVALID_GRADE['message'])
                    continue

                if grade:
                    cursor.execute("""
                        UPDATE Enrollments SET grade = ? WHERE student_id = ? AND reg_no_id = ?
                    """, (grade, student[0], reg_no_id))
                    print("Grade updated successfully.")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_reg_no_statistics(reg_no_id):
        print("\n--- reg_no Statistics ---")
        try:
            cursor = get_db_cursor()
            cursor.execute("""
                SELECT grade, COUNT(*)
                FROM Enrollments
                WHERE reg_no_id = ? AND grade IS NOT NULL
                GROUP BY grade
            """, (reg_no_id,))
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



class InstructorService:
    @staticmethod
    def view_assigned_reg_nos(instructor_id):
        """
        Fetches all reg_nos assigned to the instructor.
        """
        try:
            query = """
            SELECT reg_nos.id, reg_nos.name, reg_nos.code
            FROM reg_nos
            INNER JOIN reg_noAssignments ON reg_nos.id = reg_noAssignments.reg_no_id
            WHERE reg_noAssignments.instructor_id = ?
            """
            cursor = get_db_cursor()
            cursor.execute(query, (instructor_id,))
            reg_nos = cursor.fetchall()

            if not reg_nos:
                print("No reg_nos assigned.")
                return []

            print("\n--- Assigned reg_nos ---")
            for reg_no in reg_nos:
                print(f"reg_no ID: {reg_no[0]}, Name: {reg_no[1]}, Code: {reg_no[2]}")

            return reg_nos
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def assign_grade(student_id, reg_no_id, numeric_grade, submitted_by, comments=None):
        """
        Assigns a grade to a student for a specific reg_no.
        """
        try:
            # Find the enrollment ID for the student and reg_no
            enrollment_id_query = """
            SELECT id FROM Enrollments WHERE student_id = ? AND reg_no_id = ?
            """
            cursor = get_db_cursor()
            cursor.execute(enrollment_id_query, (student_id, reg_no_id))
            enrollment = cursor.fetchone()

            if not enrollment:
                raise ValueError(SystemErrors.DUPLICATE_ENROLLMENT['message'])

            # Create and save the grade
            grade = Grade(enrollment_id=enrollment[0], numeric_grade=numeric_grade, submitted_by=submitted_by, comments=comments)
            grade.create()
            print(f"Grade {grade.grade_value} assigned to student {student_id}.")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def view_reg_no_statistics(reg_no_id):
        """
        Displays statistics for a specific reg_no, such as average grade and grade distribution.
        """
        try:
            cursor = get_db_cursor()

            # Average grade for the reg_no
            cursor.execute("""
                SELECT AVG(numeric_grade)
                FROM Grades
                INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.id
                WHERE Enrollments.reg_no_id = ?
            """, (reg_no_id,))
            avg_grade = cursor.fetchone()[0]

            # Grade distribution for the reg_no
            cursor.execute("""
                SELECT Grades.grade_value, COUNT(*)
                FROM Grades
                INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.id
                WHERE Enrollments.reg_no_id = ?
                GROUP BY Grades.grade_value
                ORDER BY Grades.grade_value DESC
            """, (reg_no_id,))
            grade_distribution = cursor.fetchall()

            # Print the reg_no statistics
            print("\n--- reg_no Statistics ---")
            print(f"reg_no ID: {reg_no_id}")
            print(f"Average Grade: {avg_grade:.2f}" if avg_grade is not None else "No grades available for this reg_no.")

            print("\nGrade Distribution:")
            for grade, count in grade_distribution:
                print(f"Grade: {grade}, Count: {count}")
        except Exception as e:
            print(f"Error: {e}")

class ReportingService:
    @staticmethod
    def student_gpa_report(student_id):
        """
        Generates a report showing the GPA and honours classification for a student.
        """
        print("\n--- Student GPA Report ---")
        try:
            # Calculate GPA
            gpa = Grade.calculate_gpa(student_id)
            if gpa == 0.0:
                raise ValueError(f"No grades found for student {student_id}.")

            # Get honours classification
            classification = Grade.classify_honours(gpa)

            print(f"Student ID: {student_id}")
            print(f"GPA: {gpa:.2f}")
            print(f"Honours Classification: {classification}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def reg_no_statistics_report(reg_no_id):
        """
        Generates a report showing the average grade and grade distribution for a reg_no.
        """
        print("\n--- reg_no Statistics ---")
        try:
            cursor = get_db_cursor()

            # Average grade for the reg_no
            cursor.execute("""
                SELECT AVG(numeric_grade)
                FROM Grades
                INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.id
                WHERE Enrollments.reg_no_id = ?
            """, (reg_no_id,))
            avg_grade = cursor.fetchone()[0]

            # Handle case when no grades exist
            if avg_grade is None:
                raise ValueError(SystemErrors.reg_no_NOT_FOUND['message'])

            # Grade distribution for the reg_no
            cursor.execute("""
                SELECT Grades.grade_value, COUNT(*)
                FROM Grades
                INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.id
                WHERE Enrollments.reg_no_id = ?
                GROUP BY Grades.grade_value
                ORDER BY Grades.grade_value DESC
            """, (reg_no_id,))
            grade_distribution = cursor.fetchall()

            # Total number of students graded
            cursor.execute("""
                SELECT COUNT(*)
                FROM Enrollments
                WHERE reg_no_id = ?
            """, (reg_no_id,))
            total_students = cursor.fetchone()[0]

            # Print reg_no statistics
            print(f"reg_no ID: {reg_no_id}")
            print(f"Average Grade: {avg_grade:.2f}")
            print(f"Total Students Graded: {total_students}\n")
            print("Grade Distribution:")
            for grade, count in grade_distribution:
                print(f"  Grade {grade}: {count} student(s)")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
