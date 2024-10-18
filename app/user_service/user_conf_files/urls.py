# user_conf_files/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import get_data, different_name
from users.views import UserViewSet
from django.shortcuts import redirect
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


admin.site.site_header = 'Ekuchel\'s Administration'
admin.site.index_title = 'Awesome Administration stuff'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('', include(router.urls)),
   	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/data/', get_data, name='get_data'),
    path('api/code/data/', different_name, name='different_name'),
    # Redirect root URL to the login page
    path('', lambda request: redirect('/admin')),
    # This includes the login URL
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

# AVAILABLE ENDPOINTS FOR DJOSER(JWT)

# /jwt/create/ (JSON Web Token Authentication)
# /jwt/refresh/ (JSON Web Token Authentication)
# /jwt/verify/ (JSON Web Token Authentication)
# /users/
# /users/me/
# /users/confirm/
# /users/resend_activation/
# /users/set_password/
# /users/reset_password/
# /users/reset_password_confirm/
# /users/set_username/
# /users/reset_username/
# /users/reset_username_confirm/
