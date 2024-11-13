import requests
import secrets
import string
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets, status, views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny#, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin#CreateModelMixin
from .serializers import UserSerializer, PlayerProfileSerializer, MatchSerializer
from .models import User, PlayerProfile, Match
#from .permissions import IsAdminOrReadOnly
#from django.http import JsonResponse


class OAuth42LoginView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def get(self, request):
        # Generate a secure random string for the state parameter to prevent CSRF attacks
        characters = string.ascii_letters + string.digits
        state = ''.join(secrets.choice(characters) for _ in range(30))  # Adjust length as needed
        request.session['oauth_state'] = state
        # Construct the URL with query parameters
        auth_url = (
                f"{settings.API_42_AUTH_URL}"
                f"?client_id={settings.INTRA_UID_42}"
                f"&redirect_uri={settings.API_42_REDIRECT_URI}"
                f"&response_type=code"
                f"&scope=public"
                f"&state={state}"
                )
        # Redirect the user to the 42 authorization URL
        return redirect(auth_url)

def save_avatar_locally(avatar_url, player_profile, user):
    response = requests.get(avatar_url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        player_profile.avatar.save(f"{user.username}_avatar.jpg", File(img_temp), save=True)

class OAuth42CallbackView(views.APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def get(self, request):
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        session_state = request.session.get('oauth_state')

        if not code or not state:
            raise AuthenticationFailed("Missing code or state in theh callback response.")
#Validate state parameter
        if state != session_state:
            raise AuthenticationFailed("Invalid state parameter.")
# exchange code for access token
        token_response = requests.post(
                'https://api.intra.42.fr/oauth/token',
                data={
                    'grant_type': 'authorization_code',
                    'client_id': settings.INTRA_UID_42,
                    'client_secret': settings.INTRA_SECRET_42,
                    'code': code,
                    'redirect_uri': settings.API_42_REDIRECT_URI,
                    }
        )

        if token_response.status_code != 200:
            raise AuthenticationFailed("Failed to obtain access token.")

        token_data = token_response.json()
        access_token = token_data.get('access_token')

#fetch user info from 42 api
        user_info_response = requests.get(
            'https://api.intra.42.fr/v2/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if user_info_response.status_code != 200:
            raise AuthenticationFailed("Failed to obtain user information.")
        
        user_info = user_info_response.json()
        #return JsonResponse(user_info)

#get user's data
        email = user_info.get("email")
        username = user_info.get("login")
        first_name = user_info.get("first_name")
        last_name = user_info.get("last_name")
        #avatar = user_info.get("image", {}).get("link")
        avatar_url = user_info.get("image", {}).get("versions", {}).get("medium")
        displayname = user_info.get("displayname")
        provider = "42api"

#check if user exists or should be created
        user, created = User.objects.get_or_create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                auth_provider=provider,)
        
#create the player profile and store corresponding info from 42 profile.
        player_profile, profile_created = PlayerProfile.objects.get_or_create(
                user=user,
                #avatar=avatar,
                display_name=displayname,
        )
# function for downloading the image from 42api and storing it in the avatar dir.
        if avatar_url:
            save_avatar_locally(avatar_url, player_profile, user)

#Generate JWT token
        refresh = RefreshToken.for_user(user)
        try:
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'auth_provider': user.auth_provider,
                'displayname': player_profile.display_name,
                #'avatar': player_profile.avatar,  # Added avatar property
            })
        except UnicodeDecodeError as e:
            # Handle the decoding error
            return Response({
                'error': 'Unicode decoding error',
                'message': str(e)
            }, status=400)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def authorize_view(request):
    return redirect('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-000d79361be733aa7365ca50efc33b41b38c6e1b19d4f5b16456e9e63726df67&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fusers%2Fplayers%2Fme&response_type=code')

@api_view()
def say_hello(request):

    return Response('Hello from Erwin')


class PlayerProfileViewSet(RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self): #This permission setting allows any user to only see a PlayerProfiles: /users/players/1/
        if self.action == 'list' and self.request.user.is_authenticated:
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('player-profile-me')
        return Response(
            {"detail": "Please sign in into your profile."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):  # This method is called an custom action
        player_profile = PlayerProfile.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = PlayerProfileSerializer(player_profile, context=self.get_serializer_context())
            data = serializer.data
            data['username'] = request.user.username
            return Response(data)
#        if request.method == 'GET':
#            serializer = PlayerProfileSerializer(player_profile, context=self.get_serializer_context())
#            return Response(serializer.data)
# try for the automation for profile if auth_mehod is 42api then do not createa  profile
        elif request.method == 'PUT':
            serializer = PlayerProfileSerializer(
                player_profile, data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    #permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

#    def get_queryset(self):
#        if self.request.user.is_staff:
#            return Match.objects.all()
#
#        (id, created) = Match.objects.only('id').get_or_create(id=self.request.user.id)
#        return Match.objects.filter(id=id)
#return Match.objects.filter(id=self.request.user.id)
