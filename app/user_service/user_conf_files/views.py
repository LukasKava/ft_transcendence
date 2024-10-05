# user_conf_files/views.py
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
import requests
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Include additional custom fields in the token (optional)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # Custom validation logic to log in without a password
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')
        try:
            # Custom logic to find user by username or email
            user = CustomUser.objects.get(username=username_or_email) or CustomUser.objects.get(email=username_or_email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('No active account found with the given credentials')

        # You may want to do some further checks here (e.g., user.is_active)
        
        return {
            'user': user.username,
            'token': super().get_token(user),
        }

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        try:
            user = CustomUser.objects.get(username=username_or_email) or CustomUser.objects.get(email=username_or_email)
            login(request, user)
            return redirect('data_view')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid username or email')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            return redirect('login')  # Redirect to a named URL for the login page
        else:
            # Optionally, add feedback about form errors
            return render(request, 'register.html', {'form': form, 'errors': form.errors})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

class GetDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "message": "Hello from user service!"
        }
        return Response(data)

class DataView(APIView):
    permission_classes = [IsAuthenticated]  # Require JWT authentication

    def get(self, request):
        # Example data to return (replace with your actual data fetching logic)
        data = {
            'message': 'This is protected data.',
            'user': request.user.username,  # Example of accessing the authenticated user
        }
        return Response(data)