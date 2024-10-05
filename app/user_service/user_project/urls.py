# user_project/urls.py
from django.urls import path, include
from django.contrib import admin
# from django.shortcuts import redirect

urlpatterns = [
	path('admin/', admin.site.urls),
	# path('', lambda request: redirect('admin/')),
    path('api/', include('user_conf_files.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('users/', include('user_conf_files.urls')), 
]