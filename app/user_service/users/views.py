from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import UserSerializer, PlayerProfileSerializer
from .models import User, PlayerProfile
# Create your views here.


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view()
def say_hello(request):

    return Response('Hello from Erwin')


class PlayerProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self): #This permission setting allows any user to only see a PlayerProfiles: /users/players/1/
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):  # This method is called an custom action
        (player_profile, created) = PlayerProfile.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = PlayerProfileSerializer(player_profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = PlayerProfileSerializer(
                player_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
