
"""
ASGI config for country_data_project project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'country_data_project.settings')

application = get_asgi_application()
