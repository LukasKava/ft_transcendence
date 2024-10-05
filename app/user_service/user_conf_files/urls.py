# user_conf_files/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import register, CustomTokenObtainPairView

urlpatterns = [
    # JWT Authentication
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Use the custom view here
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    # API Views
    path('data/', views.DataView.as_view(), name='data_view'),  # Custom view
    path('code/data/', views.GetDataView.as_view(), name='get_data_view'),  # Custom function view
]
