import sqlite3
from app.database import DB_NAME


class BaseModel:
    """
    Base class for all models, providing connection and utility methods.
    """
    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_NAME)

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def validate_fields(self, required_fields):
        """
        Validates that all required fields are non-empty.
        """
        if any(field is None or str(field).strip() == "" for field in required_fields):
            raise ValueError("All required fields must be filled.")


class User(BaseModel):
    def __init__(self, username, password_hash, email, role):
        super().__init__()
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.role = role

    def create(self):
        query = """
        INSERT INTO Users (username, password_hash, email, role)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (self.username, self.password_hash, self.email, self.role))
        self.save()

    @staticmethod
    def find_by_username(username):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Users WHERE username = ?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        connection.close()
        return user

    def update_password(self, new_password):
        query = "UPDATE Users SET password_hash = ? WHERE username = ?"
        self.cursor.execute(query, (new_password, self.username))
        self.save()


class Student(BaseModel):
    def __init__(self, user_id, first_name, last_name, date_of_birth, admission_date, major, status):
        super().__init__()
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.admission_date = admission_date
        self.major = major
        self.status = status

    def create(self):
        self.validate_fields([self.first_name, self.last_name, self.date_of_birth, self.admission_date, self.major])
        query = """
        INSERT INTO Students (user_id, first_name, last_name, date_of_birth, admission_date, major, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.user_id, self.first_name, self.last_name, self.date_of_birth,
            self.admission_date, self.major, self.status
        ))
        self.save()


class Instructor(BaseModel):
    def __init__(self, user_id, first_name, last_name, phone, hire_date):
        super().__init__()
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.hire_date = hire_date

    def create(self):
        self.validate_fields([self.first_name, self.last_name, self.hire_date])
        query = """
        INSERT INTO Instructors (user_id, first_name, last_name, phone, hire_date)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.user_id, self.first_name, self.last_name, self.phone, self.hire_date
        ))
        self.save()


class Course(BaseModel):
    def __init__(self, course_code, title, credits, max_enrollment, prerequisites, instructor_id, status):
        super().__init__()
        self.course_code = course_code
        self.title = title
        self.credits = credits
        self.max_enrollment = max_enrollment
        self.prerequisites = prerequisites
        self.instructor_id = instructor_id
        self.status = status

    def create(self):
        self.validate_fields([self.course_code, self.title, self.credits])
        query = """
        INSERT INTO Courses (course_code, title, credits, max_enrollment, prerequisites, instructor_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.course_code, self.title, self.credits, self.max_enrollment,
            self.prerequisites, self.instructor_id, self.status
        ))
        self.save()


class Enrollment(BaseModel):
    def __init__(self, year, semester, student_id, course_id, status):
        super().__init__()
        self.year = year
        self.semester = semester
        self.student_id = student_id
        self.course_id = course_id
        self.status = status

    def create(self):
        self.validate_fields([self.year, self.semester, self.student_id, self.course_id, self.status])
        query = """
        INSERT INTO Enrollments (year, semester, student_id, course_id, status)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.year, self.semester, self.student_id, self.course_id, self.status
        ))
        self.save()


class Grade(BaseModel):
    def __init__(self, enrollment_id, grade_value, numeric_grade, submitted_by, comments):
        super().__init__()
        self.enrollment_id = enrollment_id
        self.grade_value = grade_value
        self.numeric_grade = numeric_grade
        self.submitted_by = submitted_by
        self.comments = comments

    def create(self):
        self.validate_fields([self.enrollment_id, self.grade_value])
        query = """
        INSERT INTO Grades (enrollment_id, grade_value, numeric_grade, submitted_by, comments)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.enrollment_id, self.grade_value, self.numeric_grade,
            self.submitted_by, self.comments
        ))
        self.save()
