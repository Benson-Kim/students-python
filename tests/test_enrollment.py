from app.services import StudentService
from app.services import CourseService
from app.services import enro

class TestEnrollmentWorkflow(unittest.TestCase):
    def setUp(self):
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.enrollment_service = EnrollmentService()
        self.student_service.db = ":memory:"
        self.course_service.db = ":memory:"
        self.enrollment_service.db = ":memory:"

        # Add sample student and course
        self.student_id = self.student_service.add_student({
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "2000-01-01",
            "phone": "1234567890",
            "admission_date": "2023-01-01",
            "major": "CS",
            "status": "active"
        })
        self.course_id = self.course_service.add_course({
            "course_code": "CS101",
            "title": "Intro to Computer Science",
            "credits": 3,
            "max_enrollment": 30,
            "instructor_id": 1,
            "status": "active"
        })

    def test_enrollment(self):
        result = self.enrollment_service.enroll_student(self.student_id, self.course_id, 2023, "Fall")
        self.assertTrue(result)

    def test_enrollment_with_prerequisite(self):
        self.course_service.add_course({
            "course_code": "CS102",
            "title": "Data Structures",
            "credits": 3,
            "max_enrollment": 30,
            "prerequisites": "CS101",
            "instructor_id": 1,
            "status": "active"
        })
        # Ensure prerequisite check fails
        with self.assertRaises(Exception):
            self.enrollment_service.enroll_student(self.student_id, 2, 2023, "Fall")
