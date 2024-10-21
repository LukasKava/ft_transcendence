from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, PlayerSerializer
from .models import User, Player
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


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # permission_classes = [IsAuthenticated]
