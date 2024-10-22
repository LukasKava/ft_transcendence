#add_friends/views.py


#ViewSet provides some default actions for REST API
#we have operations like: list, retrieve, create, update, partial_update adn destroy
#there are some default behaviors that might create problems


from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .services import FriendsService
from .serializers import (
    ReceiverSerializer,
    PaginationSerializer,
    RelationshipSerializer,
    UserSerializer,
    FriendshipSerializer,
)

class ManageOtherUsers(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = FriendsService()

    @action(detail=False, methods=['post'], url_path='accept-reject-invite')
    def accept_reject_invite(self, request):
        serializer = ReceiverSerializer(data=request.data)
        if serializer.is_valid():
            receiver_id = serializer.validated_data['receiver_id']
            sender_id = request.user.id  # Assuming you're using authentication
            action_type = request.data.get('action')  # 'accept' or 'reject'
            
            if action_type == 'accept':
                result, error = self.service.accept_request(sender_id, receiver_id)
            elif action_type == 'reject':
                result, error = self.service.reject_request(sender_id, receiver_id)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
            
            if error:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # List your friends with their online status
    def list(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)
        user_id = request.user.id  # Assuming you're using authentication

        friends, error = self.service.get_friends(user_id, page, limit)
        if error:
            return Response(friends, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FriendshipSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # List all users (friends or not)
    @action(detail=False, methods=['get'], url_path='list-all')
    def list_all(self, request):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        users, error = self.service.list_all_users(page, limit)
        if error:
            return Response(users, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Send a friend invite
    @action(detail=False, methods=['post'], url_path='send-invite')
    def send_invite(self, request):
        serializer = ReceiverSerializer(data=request.data)
        if serializer.is_valid():
            receiver_id = serializer.validated_data['receiver_id']
            sender_id = request.user.id  # Assuming you're using authentication

            result, error = self.service.send_invite(sender_id, receiver_id)
            if error:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Block a friend
    @action(detail=False, methods=['post'], url_path='block-friend')
    def block_friend(self, request):
        serializer = ReceiverSerializer(data=request.data)
        if serializer.is_valid():
            friend_id = serializer.validated_data['receiver_id']
            user_id = request.user.id  # Assuming you're using authentication

            result, error = self.service.block_friend(user_id, friend_id)
            if error:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
