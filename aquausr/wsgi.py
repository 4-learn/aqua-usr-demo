"""WSGI config — PythonAnywhere 用這個。"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aquausr.settings")
application = get_wsgi_application()
