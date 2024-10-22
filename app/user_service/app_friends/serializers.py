# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friendship

class ReceiverSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    limit = serializers.IntegerField(required=False, default=10)

class RelationshipSerializer(serializers.Serializer):
    players = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add other fields as needed

class FriendshipSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']
