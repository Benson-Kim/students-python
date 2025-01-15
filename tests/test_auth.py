import unittest
from app.models import User, Student, Course, Grade, Enrollment, Instructor, BaseModel
from app.database import DB_NAME

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base = BaseModel()

    def tearDown(self):
        self.base.close()

    def test_connection(self):
        conn = self.base.get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_validate_fields(self):
        with self.assertRaises(ValueError):
            self.base.validate_fields(["valid", None, "  "])
        try:
            self.base.validate_fields(["valid", "non-empty", "test"])
        except ValueError:
            self.fail("validate_fields raised ValueError unexpectedly.")

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user", "hashed_password", "student")

    def tearDown(self):
        self.user.close()

    def test_create_user(self):
        self.user.create()
        fetched_user = User.find_by_username("test_user")
        self.assertIsNotNone(fetched_user)

    def test_find_all_users(self):
        users = User.find_all()
        self.assertIsInstance(users, list)

    def test_update_password(self):
        self.user.create()
        self.user.update_password("new_hashed_password")
        updated_user = User.find_by_username("test_user")
        self.assertEqual(updated_user[2], "new_hashed_password")

class TestStudentModel(unittest.TestCase):
    def setUp(self):
        self.student = Student(1, "REG001", "John", "Doe", "2023-01-01", "CS", "active")

    def tearDown(self):
        self.student.close()

    def test_create_student(self):
        self.student.create()
        fetched_student = Student.find_by_reg_no("REG001")
        self.assertIsNotNone(fetched_student)

    def test_update_student(self):
        self.student.create()
        self.student.update(first_name="Jane")
        updated_student = Student.find_by_reg_no("REG001")
        self.assertEqual(updated_student[3], "Jane")

    def test_delete_student(self):
        self.student.create()
        Student.delete("REG001")
        fetched_student = Student.find_by_reg_no("REG001")
        self.assertIsNone(fetched_student)

class TestCourseModel(unittest.TestCase):
    def setUp(self):
        self.course = Course("CS101", "Intro to CS", 3, 30, None, "active")

    def tearDown(self):
        self.course.close()

    def test_create_course(self):
        self.course.create()
        fetched_course = Course.find_by_course_code("CS101")
        self.assertIsNotNone(fetched_course)

    def test_assign_instructor(self):
        self.course.create()
        Course.assign_instructor("CS101", 1)
        updated_course = Course.find_by_course_code("CS101")
        self.assertEqual(updated_course[4], 1)

    def test_delete_course(self):
        self.course.create()
        Course.delete("CS101")
        fetched_course = Course.find_by_course_code("CS101")
        self.assertIsNone(fetched_course)

class TestGradeModel(unittest.TestCase):
    def setUp(self):
        self.grade = Grade(enrollment_id=1, numeric_grade=85)

    def tearDown(self):
        self.grade.close()

    def test_calculate_grade(self):
        grade = self.grade.calculate_grade(85)
        self.assertEqual(grade, "A+")

    def test_classify_honours(self):
        classification = Grade.classify_honours(4.0)
        self.assertEqual(classification, "Upper Second Class Honours (2:1)")

    def test_gpa_calculation(self):
        gpa = Grade.calculate_gpa(1)
        self.assertGreaterEqual(gpa, 0.0)

if __name__ == "__main__":
    unittest.main()
