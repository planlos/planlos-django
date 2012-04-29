from django.conf.urls.defaults import *
from termine.models import Termin, Regular, Location
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail
from django.db.models import Q

info_dict = {
    'model': Termin,
    'login_required': True,
}

object_dict = {
    'queryset': Termin.objects.all().exclude(is_pub=False),
}

regular_dict = {
    'queryset': Regular.objects.all().exclude(is_pub=False).order_by('day'),
}

location_dict = {
    'queryset': Location.objects.all().exclude(name='ganz woanders!').order_by('name'),
}

def generic_pub_and_user(request, object_id):
    if request.user.is_anonymous():
        object_dict2 = Termin.objects.all().filter(is_pub=True)
    elif request.user.is_superuser:
        object_dict2 = Termin.objects.all()
    else:
        object_dict2 = Termin.objects.all().filter(Q(is_pub=True) | Q(group=request.user) )
    return object_detail(request, object_dict2, object_id)

urlpatterns = patterns('',
                       (r'^$', 'termine.views.overview'),
                       (r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'termine.views.day'),
                       #(r'termin/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', object_dict),
                       (r'termin/(?P<object_id>\d+)/', generic_pub_and_user),
                       (r'service/location/(?P<location_id>\d+)$', 'termine.service.location'    ),
                       (r'locations/$', 'django.views.generic.list_detail.object_list', location_dict),
                       (r'location/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', location_dict),
                       (r'regulars/$', 'django.views.generic.list_detail.object_list', regular_dict),
                       (r'regular/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', regular_dict),
                       (r'fast_admin/$', 'termine.views.fast_admin'),
                       (r'publish/$', 'termine.views.publish'),
                       (r'heute/$', 'termine.views.nextdays', {'diff': 0} ),
                       (r'service/heute/$', 'termine.service.heute'    ),
                       (r'service/monat/$', 'termine.service.monat'    ),
                       (r'uebermorgen/$', 'termine.views.nextdays', {'diff': 2} ),
                       (r'morgen/$', 'termine.views.nextdays', {'diff': 1} ),
                       (r'logout', 'termine.views.logout_view'),
                       (r'edit/(?P<termin_id>\d+)/$', 'termine.views.edit'),
                       (r'create', 'termine.views.create_entry'),
                       (r'create_generic', 'django.views.generic.create_update.create_object', info_dict),
                       )
