from django.test import TestCase
from users.models import User

class UserModelTestCase(TestCase):
    
    def test_user_creation(self):
        """Verifica que un usuario puede ser creado correctamente"""
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            user_type="GUEST"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword123"))
