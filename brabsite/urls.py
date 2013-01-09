from django.conf.urls import *
from django.contrib import admin
from django.views.generic import ListView, DetailView
from brabs.models import Brab
from brabs.views import BrabAddView, BrabDetailView, BrabListView
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^mybrabs/$', BrabListView.as_view(
        paginate_by=25,
        context_object_name="brab_list"),
        name="my-brab-list-view"
    ),
    url(r'^userbrabs/(?P<user_id>[a-zA-Z0-9-]+)/$', BrabListView.as_view(
        paginate_by=25,
        context_object_name="brab_list"),
        name="user-brab-list-view"
    ),
    url(r'^searchbrabs/$', BrabListView.as_view(
        paginate_by=25,
        context_object_name="brab_list"),
        name="search-brab-list-view"
    ),
    url(r'^$', ListView.as_view(
        queryset=Brab.objects.all(),
        paginate_by=25,
        context_object_name="brab_list"),
        name="all-brab-list-view"
    ),
    url(r'^addabrab/$', BrabAddView.as_view(),
        name='BrabAddView'
    ),
    url(r'^brab/(?P<pk>[a-zA-Z0-9-]+)/$', BrabDetailView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab"),
        name="brab"
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('registration.urls')),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^user_media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))