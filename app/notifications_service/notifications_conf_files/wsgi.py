# notifications_conf_files/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications_conf_files.settings')

application = get_wsgi_application()
