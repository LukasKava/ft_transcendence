from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User, PlayerProfile, Match


# for creating a new user, which information is asked
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


# for the current user, which information is shown
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email']


# Serializer for Player
class PlayerProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PlayerProfile
        fields = ['user_id', 'display_name', 'avatar',
                  'wins', 'losses', 'friends', 'online_status']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['player1', 'player2', 'winner',
                  'date', 'score_player1', 'score_player2']
