# services.py

from django.contrib.auth.models import User
from .models import Friendship
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class FriendsService:
    def add_friend(self, sender_id, receiver_id):
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)

            # Check if friendship already exists
            if Friendship.objects.filter(sender=sender, receiver=receiver).exists():
                return {"error": "Friend request already sent"}, True

            # Create a new friendship with 'pending' status
            Friendship.objects.create(sender=sender, receiver=receiver, status='pending')
            return {"message": "Friend request sent"}, False

        except ObjectDoesNotExist:
            return {"error": "User not found"}, True
        except Exception as e:
            return {"error": "An error occurred"}, True

    def accept_request(self, sender_id, receiver_id):
        try:
            friendship = Friendship.objects.get(sender_id=sender_id, receiver_id=receiver_id, status='pending')
            friendship.status = 'accepted'
            friendship.save()
            return {"message": "Friend request accepted"}, False
        except Friendship.DoesNotExist:
            return {"error": "Friend request not found"}, True
        except Exception as e:
            return {"error": "An error occurred"}, True

    def reject_request(self, sender_id, receiver_id):
        try:
            friendship = Friendship.objects.get(sender_id=sender_id, receiver_id=receiver_id, status='pending')
            friendship.status = 'rejected'
            friendship.save()
            return {"message": "Friend request rejected"}, False
        except Friendship.DoesNotExist:
            return {"error": "Friend request not found"}, True
        except Exception as e:
            return {"error": "An error occurred"}, True

    def get_friends(self, user_id, page, limit):
        try:
            friendships = Friendship.objects.filter(
                models.Q(sender_id=user_id, status='accepted') |
                models.Q(receiver_id=user_id, status='accepted')
            )
    
            if not friendships.exists():
                return [], False  # Return empty list, no error
    
            # Pagination logic
            start = (int(page) - 1) * int(limit)
            end = start + int(limit)
            paginated_friends = friendships[start:end]
    
            return paginated_friends, False
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred"}, True

    def list_all_users(self, page, limit):
        try:
            users = User.objects.all()

            # Implement pagination
            start = (int(page) - 1) * int(limit)
            end = start + int(limit)
            paginated_users = users[start:end]

            return paginated_users, False
        except Exception as e:
            return {"error": "An error occurred"}, True

    def send_invite(self, sender_id, receiver_id):
        # This could be similar to add_friend
        return self.add_friend(sender_id, receiver_id)

    def block_friend(self, user_id, friend_id):
        try:
            friendship = Friendship.objects.filter(
                models.Q(sender_id=user_id, receiver_id=friend_id) |
                models.Q(sender_id=friend_id, receiver_id=user_id)
            ).first()

            if friendship:
                friendship.status = 'blocked'
                friendship.save()
                return {"message": "Friend blocked"}, False
            else:
                return {"error": "Friendship does not exist"}, True
        except Exception as e:
            return {"error": "An error occurred"}, True
