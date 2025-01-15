# app/menus.py

from app.services import SessionManager
from app.services import AuthenticationService, StudentService, InstructorService, AdminService


def main_menu():
    print("\n--- Main Menu ---")
    print("1. Login")
    print("2. Reset Password")
    print("3. Register")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        user = AuthenticationService.login(username, password)
        if user:
            SessionManager.login_user(user)
            role_based_menu(user[3])
    elif choice == "2":
        AuthenticationService.reset_password()
    elif choice == "3":
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (default: student): ") or "student"
        success = AuthenticationService.register_user(username, password, role)
        if success:
            print("Registration successful. You're being redirected to the menu page.")
            user = AuthenticationService.login(username, password)
            if user:
                SessionManager.login_user(user)
                role_based_menu(user[3])
        else:
            print("Registration failed.")
    elif choice == "4":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")

def role_based_menu(role):
    if role == "admin":
        admin_menu()
    elif role == "instructor":
        instructor_menu()
    elif role == "student":
        student_menu()
    else:
        print("Unknown role. Logging out.")
        SessionManager.logout_user()

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Manage Students")
        print("2. Manage Courses")
        print("3. View Reports")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            # Keep the user in the Manage Students submenu until they choose to go back
            manage_students_menu()
        elif choice == "2":
            AdminService.manage_courses()
        elif choice == "3":
            AdminService.view_reports()
        elif choice == "4":
            print("Logging out...")
            SessionManager.logout_user()
            break
        else:
            print("Invalid choice. Please try again.")
            
def manage_students_menu():
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
            break  # Exit the Manage Students submenu
        else:
            print("Invalid choice. Please try again.")


def instructor_menu():
    while True:
        print("\n--- Instructor Menu ---")
        print("1. View Assigned Courses")
        print("2. Manage Grades")
        print("3. View Course Statistics")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            InstructorService.view_assigned_courses()
        elif choice == "2":
            InstructorService.manage_grades()
        elif choice == "3":
            InstructorService.view_course_statistics()
        elif choice == "4":
            print("Logging out...")
            SessionManager.logout_user()
            break
        else:
            print("Invalid choice. Please try again.")


def student_menu():
    while True:
        print("\n--- Student Menu ---")
        print("1. View Profile")
        print("2. Course Registration")
        print("3. View Grades")
        print("4. Generate Transcript")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            StudentService.view_profile()
        elif choice == "2":
            StudentService.course_registration()
        elif choice == "3":
            StudentService.view_grades()
        elif choice == "4":
            StudentService.generate_transcript()
        elif choice == "5":
            print("Logging out...")
            SessionManager.logout_user()
            break
        else:
            print("Invalid choice. Please try again.")
