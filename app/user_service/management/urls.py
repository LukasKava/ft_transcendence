from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test),
    path('', views.test),
    path('login/', views.test),
    path('logout/', views.test),
    path('register/', views.test),
]
