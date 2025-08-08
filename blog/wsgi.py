"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Run migrations and collectstatic once at startup
from django.core.management import call_command
try:
    call_command('migrate')
    call_command('collectstatic', interactive=False, verbosity=0)
except Exception as e:
    print("Startup command failed:", e)

application = get_wsgi_application()
