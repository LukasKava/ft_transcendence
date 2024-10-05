# user_project/middleware.py

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class ForceHttpsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure() and not settings.DEBUG:
            return HttpResponsePermanentRedirect(f'https://{request.get_host()}{request.path}')
        return self.get_response(request)
