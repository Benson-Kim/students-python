# app/errors.py
class SystemErrors:
    AUTH_FAILED = {'code': 1001, 'message': 'Invalid username or password'}
    SESSION_EXPIRED = {'code': 1002, 'message': 'Session expired'}
    INVALID_INPUT = {'code': 5001, 'message': 'Invalid input'}
