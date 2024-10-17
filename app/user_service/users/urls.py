from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.say_hello),
    path('login/', views.UserList.as_view()),
    path('logout/', views.UserList.as_view()),
    path('register/', views.UserList.as_view()),
]
