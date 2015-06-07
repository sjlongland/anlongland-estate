from django.conf.urls import patterns, include, url
from django.contrib import admin
import estatedb.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'estate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/*$', estatedb.views.index, name='index'),
    url(r'^all.html$', estatedb.views.all, name='all'),
    url(r'^mine.html$', estatedb.views.mine, name='mine'),
    url(r'^claimed.html$', estatedb.views.claimed, name='claimed'),
    url(r'^location/(?P<location_id>[0-9]+)/$',
        estatedb.views.location, name='location'),
    url(r'^item/(?P<item_id>[0-9]+)/$',
        estatedb.views.item, name='item'),
    url(r'^photo/(?P<photo_id>[0-9]+)/$',
        estatedb.views.photo, name='photo'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout.html$', estatedb.views.logout, name='logout'),
    url(r'^changepw.html$', estatedb.views.password_change,
        name='password_change'),
    url(r'^changedpw.html$', estatedb.views.password_change_done,
        name='password_change_done'),
)
if settings.DEBUG == True:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
