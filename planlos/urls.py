from django.conf.urls.defaults import *
from django.contrib import admin



from termine.models import Link
from termine.feeds import Termine_Syndication, Blog_Syndication, Heute_Syndication, Admin_Syndication

link_dict = {
    'queryset': Link.objects.all().order_by('category'),
}


feeds = {
    'termine': Termine_Syndication,
    'aktuelles': Blog_Syndication,
    'heute': Heute_Syndication,
    'admin_pub': Admin_Syndication,
}

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', { 'url':'/termine/'}),
    (r'^newurl/',      'planlos.blog.views.newurl'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^links/',      'django.views.generic.list_detail.object_list', dict(link_dict ) ),
    (r'^aktuelles/',       include('planlos.blog.urls')),
    (r'^termine/',        include('planlos.termine.urls')),
    (r'^polls/',        include('planlos.polls.urls')),
    # Uncomment this for admin:
    #(r'^admin/(.*)', admin.site.root),
    url(r'^admin/', include(admin.site.urls)),
    # For static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/jkur/projekte/planlos-bremen/planlosbremen.de/www/media'}),
    (r'^planlos/accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^planlos/accounts/logout/$', 'django.contrib.auth.views.logout'),
)
