import unittest
from app.services import UserService
from app.models import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user_service.db = ":memory:"  # Use in-memory database for testing

    def test_register_user(self):
        user_data = {
            "username": "testuser",
            "password": "securepassword123",
            "role": "student"
        }
        result = self.user_service.register_user(user_data)
        self.assertTrue(result)

    def test_login_valid_credentials(self):
        self.user_service.register_user({
            "username": "testuser",
            "password": "securepassword123",
            "role": "student"
        })
        session = self.user_service.login("testuser", "securepassword123")
        self.assertIsNotNone(session)

    def test_login_invalid_credentials(self):
        session = self.user_service.login("wronguser", "wrongpassword")
        self.assertIsNone(session)
