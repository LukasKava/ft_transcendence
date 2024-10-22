#app_friends/tests/tests_views.py
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from app_friends.models import Friendship

class ManageOtherUsersAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(id=2, username='user1', password='pass1')
        self.user2 = User.objects.create_user(id=3, username='user2', password='pass2')
        self.client.force_authenticate(user=self.user1)

    def test_send_invite(self):
        url = '/users/send-invite/'
        data = {'receiver_id': self.user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Friend invite sent')
        self.assertTrue(Friendship.objects.filter(sender=self.user1, receiver=self.user2).exists())

    def test_list_friends_empty(self):
        url = '/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])  # Assuming you return an empty list
