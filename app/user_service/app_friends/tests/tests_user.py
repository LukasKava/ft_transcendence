#app_friends/tests/tests_user.py
from django.test import TestCase
from django.contrib.auth.models import User

class UserCreationTest(TestCase):
    def test_create_user(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Check if the user was created successfully
        self.assertEqual(User.objects.count(), 1)
        
        # Verify the details of the user
        created_user = User.objects.get(username='testuser')
        self.assertEqual(created_user.username, 'testuser')
        self.assertTrue(created_user.check_password('testpassword'))

    def test_create_multiple_users(self):
        # Create multiple users
        User.objects.create_user(username='john', password='john')
        User.objects.create_user(username='eva', password='eva')

        # Check if the users were created successfully
        self.assertEqual(User.objects.count(), 2)
        
        # Verify their usernames
        user1 = User.objects.get(username='john')
        user2 = User.objects.get(username='eva')

        self.assertEqual(user1.username, 'john')
        self.assertEqual(user2.username, 'eva')
