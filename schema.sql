-- Users Table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'instructor', 'student')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Students Table
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    reg_no TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    admission_date DATE NOT NULL,
    major TEXT,
    status TEXT CHECK(status IN ('active', 'inactive', 'graduated', 'suspended')) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Instructors Table
CREATE TABLE Instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    staff_no TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    hire_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Courses Table
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    credits INTEGER NOT NULL,
    max_enrollment INTEGER NOT NULL,
    prerequisites TEXT,
    instructor_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('active', 'inactive', 'archived')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)
);

-- Enrollments Table
CREATE TABLE Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    semester TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('enrolled', 'withdrawn', 'completed')) NOT NULL,
    withdrawal_date TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    UNIQUE(student_id, course_id, year, semester)
);

-- Grades Table
CREATE TABLE Grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER NOT NULL,
    grade_value TEXT,
    numeric_grade DECIMAL(4,2),
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_by INTEGER NOT NULL,
    comments TEXT,
    FOREIGN KEY (enrollment_id) REFERENCES Enrollments(enrollment_id),
    FOREIGN KEY (submitted_by) REFERENCES Instructors(instructor_id)
);
