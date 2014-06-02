import os
import sys
import site

site.addsitedir('/home/planlos/planlos-django/env/lib/python2.7/site-packages')

sys.path.append('/home/planlos/planlos-django/')
sys.path.append('/home/planlos/planlos-django/planlos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'planlos.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
