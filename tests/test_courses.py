from app.services import CourseService
from app.models import Course

class TestCourseService(unittest.TestCase):
    def setUp(self):
        self.course_service = CourseService()
        self.course_service.db = ":memory:"  # Use in-memory database for testing

    def test_add_course(self):
        course_data = {
            "course_code": "CS101",
            "title": "Intro to Computer Science",
            "credits": 3,
            "max_enrollment": 30,
            "instructor_id": 1,
            "status": "active"
        }
        result = self.course_service.add_course(course_data)
        self.assertTrue(result)

    def test_add_course_duplicate_code(self):
        course_data = {
            "course_code": "CS101",
            "title": "Intro to Computer Science",
            "credits": 3,
            "max_enrollment": 30,
            "instructor_id": 1,
            "status": "active"
        }
        self.course_service.add_course(course_data)
        with self.assertRaises(Exception):
            self.course_service.add_course(course_data)
