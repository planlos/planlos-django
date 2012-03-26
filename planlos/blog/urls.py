from django.conf.urls.defaults import *
from blog.models import Entry

info_dict = {
    'queryset': Entry.objects.all().order_by('-pub_date'),
}

modify_dict = {
    'model': Entry,
    'login_required': True,
    }

urlpatterns = patterns('',
                       #(r'(?P<page>\d+)$', 'django.views.generic.list_detail.object_list', dict(info_dict, paginate_by=4)),
                       (r'$', 'django.views.generic.list_detail.object_list', dict(info_dict, paginate_by=4)),

                       (r'create/?$', 'django.views.generic.create_update.create_object', dict(modify_dict, post_save_redirect="/aktuelles/")),
                       )
