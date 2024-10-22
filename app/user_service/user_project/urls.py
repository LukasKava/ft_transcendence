# user_project/urls.py
from django.urls import path, include

urlpatterns = [
    # path('api/', include('user_conf_files.urls')),
	path('friends/', include('app_friends.urls')), 
]