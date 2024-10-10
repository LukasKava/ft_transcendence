from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# Create your views here.

@api_view(['GET', 'POST'])
def user_management(request):
    if request.method == "GET":
        return Response('GET method requested')
    elif request.method == 'POST':
        return Response('POST method requested')


