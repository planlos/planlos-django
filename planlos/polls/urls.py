#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from polls.models import Poll, Choice

admin.autodiscover()

poll_dict = {
    'queryset': Poll.objects.all().order_by('pub_date'),
}

urlpatterns = patterns('',
#    (r'(?P<pollid>\d+)/$', 'django.views.generic.list_detail.object_detail', poll_detail_dict),
    (r'(?P<pollid>\d+)/$', 'polls.views.show_poll'),
    (r'(?P<pollid>\d+)/vote/$', 'polls.views.vote'),
    (r'(?P<pollid>\d+)/results/$', 'polls.views.show_results'),
    (r'$', 'django.views.generic.list_detail.object_list', poll_dict),
)
