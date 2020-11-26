"""
WSGI config for mytoolproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from wsgi_basic_auth import BasicAuth # 追加 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('WSGI_AUTH_CREDENTIALS', '[ID]:[PW]')

application = get_wsgi_application()

application = BasicAuth(application)
