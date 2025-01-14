# app/errors.py
class SystemErrors:
    AUTH_FAILED = {
        'code': 1001,
        'message': 'Invalid username or password',
        'severity': 'WARNING'
    }
    SESSION_EXPIRED = {
        'code': 1002,
        'message': 'Your session has expired. Please login again',
        'severity': 'INFO'
    }
    INSUFFICIENT_PERMISSIONS = {
        'code': 1003,
        'message': 'You do not have permission to perform this action',
        'severity': 'WARNING'
    }

    # Student Management Errors (2000-2999)
    ENROLLMENT_LIMIT = {
        'code': 2001,
        'message': 'Course has reached maximum enrollment capacity',
        'severity': 'WARNING'
    }
    PREREQUISITE_NOT_MET = {
        'code': 2002,
        'message': 'Required prerequisites are not satisfied',
        'severity': 'WARNING'
    }
    DUPLICATE_ENROLLMENT = {
        'code': 2003,
        'message': 'Student is already enrolled in this course',
        'severity': 'WARNING'
    }

    # Grade Management Errors (3000-3999)
    INVALID_GRADE = {
        'code': 3001,
        'message': 'Invalid grade value provided',
        'severity': 'ERROR'
    }
    GRADE_DEADLINE_PASSED = {
        'code': 3002,
        'message': 'Grade submission deadline has passed',
        'severity': 'WARNING'
    }
    UNAUTHORIZED_GRADE_CHANGE = {
        'code': 3003,
        'message': 'Unauthorized to modify grades for this course',
        'severity': 'ERROR'
    }

    # Course Management Errors (4000-4999)
    INVALID_COURSE_CODE = {
        'code': 4001,
        'message': 'Invalid course code format',
        'severity': 'ERROR'
    }
    COURSE_NOT_FOUND = {
        'code': 4002,
        'message': 'Requested course does not exist',
        'severity': 'ERROR'
    }
    SCHEDULE_CONFLICT = {
        'code': 4003,
        'message': 'Course schedule conflicts with existing enrollment',
        'severity': 'WARNING'
    }

    # Data Validation Errors (5000-5999)
    INVALID_INPUT = {
        'code': 5001,
        'message': 'Invalid input provided',
        'severity': 'WARNING'
    }
    REQUIRED_FIELD_MISSING = {
        'code': 5002,
        'message': 'Required field(s) missing',
        'severity': 'ERROR'
    }
    DATA_FORMAT_ERROR = {
        'code': 5003,
        'message': 'Invalid data format',
        'severity': 'ERROR'
    }
