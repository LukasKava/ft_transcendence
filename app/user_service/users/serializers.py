from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User, PlayerProfile, Match, PlayerMatch


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
    profile_id = serializers.IntegerField(read_only=True, source='id')

    class Meta:
        model = PlayerProfile
        fields = ['user_id', 'display_name', 'avatar',
                  'wins', 'losses', 'profile_id', 'friends', 'matches'] # 'online_status'

class SimplePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerProfile
        fields = ['display_name', 'avatar', 'id']


class PlayerMatchSerializer(serializers.ModelSerializer):
    player = PlayerProfileSerializer(read_only=True)

    class Meta:
        model = PlayerMatch
        fields = ['player', 'date', 'match']


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerMatchSerializer(source='playermatch_set', many=True, read_only=True)
#    player1 = PlayerProfileSerializer()
#    player2 = PlayerProfileSerializer()

    class Meta:
        model = Match
        fields = ['id', 'date', 'player1', 'player2',
                  'winner', 'score_player1', 'score_player2', 'players']
