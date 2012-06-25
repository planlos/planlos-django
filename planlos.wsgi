import os
import sys

sys.path.append('/home/planlos/planlos-django/')
sys.path.append('/home/planlos/planlos-django/planlos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'planlos.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
