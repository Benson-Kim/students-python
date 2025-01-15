import unittest
from app.services import (
    AuthenticationService,
    AdminService,
    StudentService,
    CourseService,
    ReportingService
)
from app.models import User, Student, Course

class TestAuthenticationService(unittest.TestCase):
    def test_register_user(self):
        result = AuthenticationService.register_user("test_user", "test_password")
        self.assertTrue(result)

    def test_login(self):
        AuthenticationService.register_user("test_user", "test_password")
        user = AuthenticationService.login("test_user", "test_password")
        self.assertIsNotNone(user)

    def test_reset_password(self):
        AuthenticationService.register_user("test_user", "test_password")
        result = AuthenticationService.reset_password("test_user", "new_password")
        self.assertTrue(result)

class TestAdminService(unittest.TestCase):
    def test_manage_students(self):
        StudentService.add_student()
        students = Student.find_all()
        self.assertGreater(len(students), 0)

    def test_manage_courses(self):
        CourseService.add_course()
        courses = Course.find_all()
        self.assertGreater(len(courses), 0)

class TestStudentService(unittest.TestCase):
    def test_add_student(self):
        StudentService.add_student()
        students = Student.find_all()
        self.assertGreater(len(students), 0)

    def test_delete_student(self):
        StudentService.add_student()
        StudentService.delete_student()
        students = Student.find_all()
        self.assertEqual(len(students), 0)

class TestCourseService(unittest.TestCase):
    def test_add_course(self):
        CourseService.add_course()
        courses = Course.find_all()
        self.assertGreater(len(courses), 0)

    def test_assign_instructor(self):
        CourseService.add_course()
        CourseService.assign_instructor_to_course("CS101")
        courses = Course.find_all()
        self.assertIsNotNone(courses[0][4])

class TestReportingService(unittest.TestCase):
    def test_student_gpa_report(self):
        result = ReportingService.student_gpa_report(1)
        self.assertIsNotNone(result)

    def test_course_statistics_report(self):
        result = ReportingService.reg_no_statistics_report(1)
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
