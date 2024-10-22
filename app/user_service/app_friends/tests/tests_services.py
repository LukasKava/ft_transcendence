#app_friends/tests/tests_services.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from app_friends.services import FriendsService
from app_friends.models import Friendship

class FriendsServiceTest(TestCase):
    def setUp(self):
        self.service = FriendsService()
        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')

    def test_add_friend_success(self):
        response, error = self.service.add_friend(self.user1.id, self.user2.id)
        self.assertFalse(error)
        self.assertEqual(response['message'], "Friend request sent")
        self.assertTrue(Friendship.objects.filter(sender=self.user1, receiver=self.user2).exists())

    def test_add_friend_already_exists(self):
        Friendship.objects.create(sender=self.user1, receiver=self.user2, status='pending')
        response, error = self.service.add_friend(self.user1.id, self.user2.id)
        self.assertTrue(error)
        self.assertEqual(response['error'], "Friend request already sent")
