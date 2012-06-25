import os
import sys

sys.path.append('/home/planlos/planlos-django-test/')
sys.path.append('/home/planlos/planlos-django-test/planlos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'planlos.settings_test'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
