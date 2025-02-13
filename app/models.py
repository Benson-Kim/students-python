# app/models.py

import sqlite3
from app.database import DB_NAME

# Grading system with honours classifications
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

HONOURS_CLASSIFICATIONS = {
    'First Class': {'min_average': 70, 'description': 'First Class Honours (1st)'},
    'Upper Second': {'min_average': 60, 'description': 'Upper Second Class Honours (2:1)'},
    'Lower Second': {'min_average': 50, 'description': 'Lower Second Class Honours (2:2)'},
    'Third': {'min_average': 40, 'description': 'Third Class Honours (3rd)'},
    'Fail': {'min_average': 0, 'description': 'Fail'}
}

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
    def __init__(self, username, password_hash, role):
        super().__init__()
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def create(self):
        query = """
        INSERT INTO Users (username, password_hash, role)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(query, (self.username, self.password_hash, self.role))
        self.save()
    
    @staticmethod
    def find_all():
        """
        Retrieves all users from the database.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Users"
        cursor.execute(query)
        users = cursor.fetchall()
        connection.close()
        return users

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
    def __init__(self, user_id, reg_no, first_name, last_name, admission_date, major, status):
        super().__init__()
        self.user_id = user_id
        self.reg_no = reg_no 
        self.first_name = first_name
        self.last_name = last_name
        self.admission_date = admission_date
        self.major = major
        self.status = status

    def create(self):
        self.validate_fields([self.reg_no, self.first_name, self.last_name, self.admission_date, self.major])
        query = """
        INSERT INTO Students (user_id, reg_no, first_name, last_name, admission_date, major, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.user_id, self.reg_no, self.first_name, self.last_name, 
            self.admission_date, self.major, self.status
        ))
        self.save()

    @staticmethod
    def find_by_reg_no(reg_no):
        """
        Retrieve a student by registration number.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Students WHERE reg_no = ?"
        cursor.execute(query, (reg_no,))
        student = cursor.fetchone()
        connection.close()
        return student
    
    @staticmethod
    def find_all():
        """
        Retrieves all students from the database.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Students"
        cursor.execute(query)
        students = cursor.fetchall()
        connection.close()
        return students

    def update(self, first_name=None, last_name=None, major=None, status=None):
        """
        Update student details.
        """
        query = """
        UPDATE Students
        SET first_name = ?, last_name = ?, major = ?, status = ?
        WHERE reg_no = ?
        """
        self.cursor.execute(query, (first_name, last_name, major, status, self.reg_no))
        self.save()

    @staticmethod
    def delete(reg_no):
        """
        Delete a student by registration number.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM Students WHERE reg_no = ?"
        cursor.execute(query, (reg_no,))
        connection.commit()
        connection.close()



class Instructor(BaseModel):
    def __init__(self, user_id, staff_no, first_name, last_name, hire_date):
        super().__init__()
        self.user_id = user_id
        self.staff_no = staff_no
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date

    def create(self):
        self.validate_fields([self.staff_no, self.first_name, self.last_name, self.hire_date])
        query = """
        INSERT INTO Instructors (user_id, staff_no, first_name, last_name, hire_date)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.user_id, self.staff_no, self.first_name, self.last_name, self.hire_date
        ))
        self.save()
    
    @staticmethod
    def find_all():
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT instructor_id, first_name, last_name FROM Instructors"
        cursor.execute(query)
        instructors = cursor.fetchall()
        connection.close()
        return instructors
    
    @staticmethod
    def get_name_by_id(instructor_id):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT first_name, last_name FROM Instructors WHERE instructor_id = ?"
        cursor.execute(query, (instructor_id,))
        instructor = cursor.fetchone()
        connection.close()
        return f"{instructor[0]} {instructor[1]}" if instructor else "Unassigned"

    @staticmethod
    def get_course_count(instructor_id):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM Courses WHERE instructor_id = ?"
        cursor.execute(query, (instructor_id,))
        count = cursor.fetchone()[0]
        connection.close()
        return count
    
    @staticmethod
    def get_assigned_courses(instructor_id):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = """
                SELECT course_id, course_code, title, credits, max_enrollment
                FROM Courses
                WHERE instructor_id = ?
            """
        cursor.execute(query, (instructor_id,))
        courses = cursor.fetchall()
        connection.close()
        return courses
    
    @staticmethod
    def view_course_statistics(instructor_id):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = """
                SELECT c.course_code, c.course_name 
                FROM Courses c
                WHERE c.instructor_id = ?
            """
        cursor.execute(query, (instructor_id,))
        courses = cursor.fetchall()
        connection.close()
        return courses




class Course(BaseModel):
    def __init__(self, course_code, title, credits, max_enrollment, instructor_id, status):
        super().__init__()
        self.course_code = course_code
        self.title = title
        self.credits = credits
        self.max_enrollment = max_enrollment
        self.instructor_id = instructor_id
        self.status = status

    def create(self):
        self.validate_fields([self.course_code, self.title, self.credits])
        query = """
        INSERT INTO Courses (course_code, title, credits, max_enrollment, instructor_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.course_code, self.title, self.credits, self.max_enrollment,
            self.instructor_id, self.status
        ))
        self.save()
    
    @staticmethod
    def find_by_course_code(course_code):
        """
        Retrieve a course by course code.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Courses WHERE course_code = ? AND status = 'active'"
        cursor.execute(query, (course_code,))
        course = cursor.fetchone()
        connection.close()
        return course
    
    @staticmethod
    def find_all():
        """
        Retrieves all courses from the database.
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = """
            SELECT c.course_code, c.title, c.credits, c.max_enrollment, 
                i.staff_no, i.first_name || ' ' || i.last_name AS instructor_name
            FROM Courses c
            LEFT JOIN Instructors i ON c.instructor_id = i.instructor_id
            WHERE c.status='active';
        """
        cursor.execute(query)
        courses = cursor.fetchall()
        connection.close()
        return courses

    def update(self, title=None, credits=None, max_enrollment=None, status=None):
        """
        Update course details.
        """
        query = """
        UPDATE Courses
        SET title = ?, credits = ?, max_enrollment = ?, status = ?
        WHERE course_code = ?
        """

        self.cursor.execute(query, (title, credits, max_enrollment, status, self.course_code))
        self.save()

    @staticmethod
    def delete(course_code):
        """
        Delete a course by course code
        """
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM Courses WHERE course_code = ?"
        cursor.execute(query, (course_code,))
        connection.commit()
        connection.close()

    @staticmethod
    def assign_instructor(course_code, instructor_id):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = "UPDATE Courses SET instructor_id = ? WHERE course_code = ?"
        cursor.execute(query, (instructor_id, course_code))
        connection.commit()
        connection.close()
    
    @staticmethod
    def get_course_aggregates(course_code):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = """
            SELECT AVG(ec.grade) as avg_grade, COUNT(ec.student_id) as total_students
            FROM Enrollments ec
            WHERE ec.course_code = ?
            """
        cursor.execute(query, (course_code))
        aggregates = cursor.fetchone()
        connection.close()
        return aggregates

    @staticmethod
    def get_course_students(course_code):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = """
            SELECT s.registration_number, s.first_name, s.last_name, ec.grade
            FROM Students s
            JOIN Enrollments ec ON s.id = ec.student_id
            WHERE ec.course_code = ?
            """
        cursor.execute(query, (course_code))
        students = cursor.fetchall()
        connection.close()
        return students   


class Enrollment(BaseModel):
    def __init__(self, enrollment_id, year, semester, student_id, course_id, status):
        super().__init__()

        self.enrollment_id = enrollment_id
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


    @staticmethod
    def get_enrollment_statistics_for_all_courses():
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = ("""
            SELECT c.course_code, c.title, COUNT(e.student_id)
            FROM Enrollments e
            INNER JOIN Courses c ON e.course_id = c.course_id
            WHERE c.status = 'active'
            GROUP BY c.course_code, c.title
        """)
        cursor.execute(query)
        courses_enrollment_stats = cursor.fetchall()
        connection.close()
        return courses_enrollment_stats


    @staticmethod
    def get_enrollment_statistics_for_course(course_code):
        connection = BaseModel.get_connection()
        cursor = connection.cursor()
        query = ("""
            SELECT c.course_code, c.title, COUNT(e.student_id)
            FROM Enrollments e
            INNER JOIN Courses c ON e.course_id = c.course_id
            WHERE c.course_code = ? AND c.status = 'active'
            GROUP BY c.course_code, c.title
        """)
        cursor.execute(query, (course_code,))
        course_enrollment_stats = cursor.fetchall()
        connection.close()
        return course_enrollment_stats


class Grade(BaseModel):
    def __init__(self, enrollment_id, grade_value=None, numeric_grade=None, submitted_by=None, comments=None):
        super().__init__()
        self.enrollment_id = enrollment_id
        self.grade_value = grade_value or self.calculate_grade(numeric_grade)
        self.numeric_grade = numeric_grade
        self.submitted_by = submitted_by
        self.comments = comments

    def calculate_grade(self, numeric_grade):
        for grade, details in GRADE_POINTS.items():
            range_min, range_max = map(int, details['range'].split('-'))
            if range_min <= numeric_grade <= range_max:
                return grade
        return 'F'

    def create(self):
        self.validate_fields([self.enrollment_id, self.numeric_grade])
        query = """
        INSERT INTO Grades (enrollment_id, grade_value, numeric_grade, submitted_by, comments)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            self.enrollment_id, self.grade_value, self.numeric_grade,
            self.submitted_by, self.comments
        ))
        self.save()

    @staticmethod
    def calculate_gpa(student_id):
        query = """
        SELECT numeric_grade FROM Grades
        INNER JOIN Enrollments ON Grades.enrollment_id = Enrollments.id
        WHERE Enrollments.student_id = ?
        """
        cursor = BaseModel.get_connection().cursor()
        cursor.execute(query, (student_id,))
        grades = cursor.fetchall()

        if not grades:
            return 0.0

        total_points = sum(GRADE_POINTS[Grade(None).calculate_grade(grade[0])]['points'] for grade in grades)
        return round(total_points / len(grades), 2)

    @staticmethod
    def classify_honours(gpa):
        for classification, details in HONOURS_CLASSIFICATIONS.items():
            if gpa >= details['min_average']:
                return details['description']
        return HONOURS_CLASSIFICATIONS['Fail']['description']