# app/services.py

from app.models import User, Student, Grade, Enrollment, Course, Instructor
from app.utils import verify_password, hash_password

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
    
    @staticmethod
    def get_logged_in_user_id():
        if SessionManager.current_user:
            return SessionManager.current_user[0]
        return None


class AdminService:
    @staticmethod
    def manage_students():
        """
        Display and handle the 'Manage Students' menu.
        Delegates actions to the appropriate methods in StudentService.
        """
        while True:
            print("\n--- Manage Students ---")
            print("1. View All Students")
            print("2. Add Student")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Go Back")

            choice = input("Choose an option: ")

            if choice == "1":
                StudentService.view_all_students()
            elif choice == "2":
                StudentService.add_student()
            elif choice == "3":
                StudentService.update_student()
            elif choice == "4":
                StudentService.delete_student()
            elif choice == "5":
                print("Returning to Admin Menu...")
                break
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def manage_courses():
        """
        Display and handle the 'Manage Courses' menu.
        Delegates actions to the appropriate methods in CourseService.
        """
        while True:
            print("\n--- Manage Courses ---")
            print("1. View All Courses")
            print("2. Add Course")
            print("3. Update Course")
            print("4. Delete Course")
            print("5. Assign Instructor to Course")
            print("6. Go Back")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                CourseService.view_all_courses()
            elif choice == "2":
                CourseService.add_course()
            elif choice == "3":
                CourseService.update_course()
            elif choice == "4":
                CourseService.delete_course()
            elif choice == "5":
                course_code = input("Enter Course Code: ").strip()
                CourseService.assign_instructor_to_course(course_code)
            elif choice == "6":
                print("Returning to Admin Menu...")
                break
            else:
                print("Invalid option. Please try again.")

    @staticmethod
    def view_reports():
        """
        Display and handle the 'View Reports' menu.
        Delegates actions to the appropriate methods in AdminService or CourseService.
        """
        while True:
            print("\n--- View Reports ---")
            print("1. View Student Transcripts")
            print("2. View Course List")
            print("3. View Enrollment Statistics")
            print("4. View Specific Course Enrollment Statistics")
            print("5. Go Back")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                AdminService.view_student_transcripts()
            elif choice == "2":
                CourseService.view_all_courses()
            elif choice == "3":
                AdminService.get_all_courses_enrollment_statistics()
            elif choice == "4":
                AdminService.get_specific_course_enrollment_statistics()
            elif choice == "5":
                print("Returning to Admin Menu...")
                break
            else:
                print("Invalid option. Please try again.")

       
    
    @staticmethod
    def view_student_transcripts():
       
       print("Feature to implement: View student transcripts")


    @staticmethod
    def get_all_courses_enrollment_statistics():
        print("\n--- Enrollment Statistics for All Courses ---")
        try:
            stats = Enrollment.get_enrollment_statistics_for_all_courses()

            if stats:
                print(f"{'Course Code':<15} {'Course Title':<30} {'Enrolled Students':<20}")
                print("-" * 65)  
                for course_code, title, enrollment_count in stats:
                    print(f"{course_code:<15} {title:<30} {enrollment_count:<20}")
            else:
                print("No enrollment statistics available for any courses.")
        except Exception as e:
            print(f"Error fetching statistics: {e}")

    @staticmethod
    def get_specific_course_enrollment_statistics(course_code):
        print(f"\n--- Enrollment Statistics for Course: {course_code} ---")
        try:
            stats = Enrollment.get_enrollment_statistics_for_course(course_code)

            if stats:
                print(f"{'Course Code':<15} {'Course Title':<30} {'Enrolled Students':<20}")
                print("-" * 65)  
                for course_code, title, enrollment_count in stats:
                    print(f"{course_code:<15} {title:<30} {enrollment_count:<20}")
            else:
                print(f"No enrollment statistics available for course code: {course_code}")
        except Exception as e:
            print(f"Error fetching statistics for course {course_code}: {e}")




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
                print(f"{'Reg No':<20} {'Name':<30} {'Major':<20} {'Status':<15}")
                print("-" * 85) 
                for student in students:
                    reg_no = student[2]
                    name = f"{student[3]} {student[4]}"
                    major = student[6]
                    status = student[7]
                    print(f"{reg_no:<20} {name:<30} {major:<20} {status:<15}")
            else:
                print("No students found.")
        except Exception as e:
            print(f"Error: {e}")


    @staticmethod
    def update_student():
        print("\n--- Update Student Details ---")
        reg_no = input("Enter Registration Number: ")

        student_data = Student.find_by_reg_no(reg_no)
        if not student_data:
            print("Student not found.")
            return

        student_id, user_id, reg_no, first_name, last_name, admission_date, major, status = student_data

        print("Leave field blank to keep current value.")
        first_name = input(f"First Name [{first_name}]: ") or first_name
        last_name = input(f"Last Name [{last_name}]: ") or last_name
        major = input(f"Major [{major}]: ") or major
        status = input(f"Status [{status}]: ") or status

        try:
            student_instance = Student( user_id, reg_no, first_name, last_name, admission_date, major, status)

            student_instance.update(first_name, last_name, major, status)
            print("Student updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    
    @staticmethod
    def delete_student():
        print("\n--- Delete Student ---")
        reg_no = input("Enter Registration Number: ")

        try:
            student_data = Student.find_by_reg_no(reg_no)
            if not student_data:
                print("Student not found.")
                return
            
            Student.delete(reg_no)
            print("Student deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
    
    @staticmethod
    def view_profile(reg_no):
        print("Feature to implement: View student profile")
    
    @staticmethod
    def course_registration(reg_no):
        print("Feature to implement: enroll in courses")
    
    @staticmethod
    def view_grades(reg_no):
        print("Feature to implement: View personal grades")
    
    @staticmethod
    def generate_transcript(reg_no):
        print("Feature to implement: generate student transcript")

class CourseService:
    @staticmethod
    def add_course():
        print("\n--- Add New Course ---")
        course_code = input("Course Code: ")
        title = input("Course Title: ")
        credits = input("Credits: ")
        max_enrollment = input("Max Enrollment: ")
        status = input("Status (active/inactive): ").lower() or "active"

        try:
            # Create the course without assigning an instructor
            course = Course(course_code, title, credits, max_enrollment, None, status)
            course.create()
            print("Course added successfully.")

            CourseService.assign_instructor_to_course(course_code)

        except Exception as e:
            print(f"Error adding course: {e}")

    @staticmethod
    def view_all_courses():
        try:
            courses = Course.find_all()
            if courses:
                print("\n--- All Courses ---")
                print(f"{'Course Code':<15} {'Title':<30} {'Credits':<10} {'Max Enrollment':<15} {'Instructor Name':<30}")
                print("-" * 100)  
                
                for course in courses:
                    course_code = course[0]
                    title = course[1]
                    credits = str(course[2])
                    max_enrollment = str(course[3])
                    instructor = course[4] if course[4] else "No instructor assigned"
                    print(f"{course_code:<15} {title:<30} {credits:<10} {max_enrollment:<15} {instructor:<30}")
            else:
                print("No courses found.")
        except Exception as e:
            print(f"Error retrieving courses: {e}")

    @staticmethod
    def update_course():
        print("\n--- Update Course Details ---")
        course_code = input("Enter Course Code: ")

        course_data = Course.find_by_course_code(course_code)
        if not course_data:
            print("Course not found.")
            return

        course_id, course_code, title, credits, max_enrollment, instructor_id, status = course_data

        print("Leave field blank to keep current value.")
        title = input(f"Title [{title}]: ") or title
        credits = input(f"Credits [{credits}]: ") or credits
        max_enrollment = input(f"Max Enrollment [{max_enrollment}]: ") or max_enrollment
        status = input(f"Status [{status}]: ") or status

        try:
            course_instance = Course(course_code, title, credits, max_enrollment, instructor_id, status)
            course_instance.update(title=title, credits=credits, max_enrollment=max_enrollment, status=status)
            print("Course updated successfully.")
        except Exception as e:
            print(f"Error updating course: {e}")
    
    @staticmethod
    def delete_course():
        print("\n--- Delete Course ---")
        course_code = input("Enter Course Code: ")

        try:
            course_data = Course.find_by_course_code(course_code)
            if not course_data:
                print("Course not found.")
                return
            
            Course.delete(course_code)
            print("Course deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
    
    @staticmethod
    def assign_instructor_to_course(course_code):
        print(f"\n--- Assign Instructor to Course: {course_code} ---")
        instructors = Instructor.find_all()  

        if not instructors:
            print("No instructors found.")
            choice = input("Would you like to add a new instructor? (yes/no): ").strip().lower()
            if choice == 'yes':
                    InstructorService.add_instructor()
                    CourseService.assign_instructor_to_course(course_code)
            return


        print("\nAvailable Instructors:")
        for idx, instructor in enumerate(instructors, start=1):
            instructor_id, first_name, last_name = instructor[:3]
            assigned_courses = Instructor.get_course_count(instructor_id) 
            print(f"{idx}. {first_name} {last_name} (Courses Assigned: {assigned_courses})")


        try:
            selection = int(input("Select an instructor by number: "))
            if 1 <= selection <= len(instructors):
                instructor_id = instructors[selection - 1][0]

                Course.assign_instructor(course_code, instructor_id)
                print(f"Instructor assigned successfully to course {course_code}.")
            else:
                print("Invalid selection. Try again.")
                CourseService.assign_instructor_to_course(course_code) 
        except ValueError:
            print("Invalid input. Please enter a number.")
            CourseService.assign_instructor_to_course(course_code)  


    @staticmethod
    def assign_instructor_to_new_course():
        print("\n--- Assign Instructor to a Course ---")
        courses = Course.find_all()

        if not courses:
            print("No courses found.")
            return

        print("\nAvailable Courses:")
        for idx, course in enumerate(courses, start=1):
            print(f"{idx}. {course[1]} ({course[2]})")

        try:
            selection = int(input("Select a course by number: "))
            if 1 <= selection <= len(courses):
                course_code = courses[selection - 1][1]
                instructor_id = input("Enter Instructor ID: ")
                Course.assign_instructor(course_code, instructor_id)
                print(f"Instructor assigned to course {course_code}.")
            else:
                print("Invalid selection. Try again.")
                CourseService.assign_instructor_to_new_course()
        except ValueError:
            print("Invalid input. Please enter a number.")
            CourseService.assign_instructor_to_new_course()



class InstructorService:
    @staticmethod
    def add_instructor():
        print("\n--- Register New Instructor ---")

        try:
            username = input("Username: ")
            password = input("Password: ")
            user = User(username, hash_password(password), "instructor")
            user.create()

            user_id = user.cursor.lastrowid
            staff_no = input("Staff Number: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            hire_date = input("Hire Date (YYYY-MM-DD): ")
        
            instructor = Instructor(user_id, staff_no, first_name, last_name, hire_date)
            instructor.create()
            print("Instructor added successfully.")
        except Exception as e:
            print(f"Error adding instructor: {e}")
    
    @staticmethod
    def view_assigned_courses():
        try:
            courses = Instructor.get_assigned_courses(SessionManager.get_logged_in_user_id())
            if courses:
                print("\n--- Assigned Courses ---")
                print(f"{'Course Code':<15} {'Title':<30} {'Credits':<10} {'Max Enrollment':<15}")
                print("-" * 80)  
                
                for course in courses:
                    course_code = course[1]
                    title = course[2]
                    credits = str(course[3])
                    max_enrollment = str(course[4])
                    print(f"{course_code:<15} {title:<30} {credits:<10} {max_enrollment:<15}")
            else:
                print("No courses found.")
        except Exception as e:
            print(f"Error retrieving courses: {e}")

    @staticmethod
    def assign_grade(student_id, reg_no_id, numeric_grade, submitted_by, comments=None):
        """
        Assigns a grade to a student for a specific reg_no.
        """
       
        print("Feature to implement: Update the grade for the student")

    @staticmethod
    def view_assigned_course_statistics():
        """
        Displays statistics for a course, such as average grade and grade distribution and the students enrolled.
        """

        print("Feature to implement: View statistics for a specific course")
        

class ReportingService:
    @staticmethod
    def student_gpa_report(student_id):
        """
        Generates a report showing the GPA and honours classification for a student.
        """

        print("Feature to implement: Generate student GPA report")

    @staticmethod
    def reg_no_statistics_report(reg_no_id):
        """
        Generates a report showing the average grade and grade distribution for a reg_no.
        """
        
        print("Feature to implement: Generate reg_no statistics report")
