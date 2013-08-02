from django.conf.urls import *
from django.contrib import admin
from django.views.generic import ListView, DetailView
from brabs.models import Brab
from brabs.views import hello, BrabAddView, BrabDetailView, BrabListView, BrabEditView, Follower_to_followeeListView, Followee_to_followerListView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^hello/$', view=hello, name='hello_page'
    ),
    url(r'^followers/$', Followee_to_followerListView.as_view(
        paginate_by=20,
        context_object_name="follower_list"),
        name="follower-list-view"
    ),
    url(r'^followees/$', Follower_to_followeeListView.as_view(
        paginate_by=20,
        context_object_name="followee_list"),
        name="followee-list-view"
    ),
    url(r'^fwbrabs/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="fw-brab-list-view"
    ),
    url(r'^envybrabs/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="my-envy-brab-list-view"
    ),
    url(r'^mybrabs/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="my-brab-list-view"
    ),
    url(r'^userbrabs/(?P<user_id>[a-zA-Z0-9-]+)/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="user-brab-list-view"
    ),
    url(r'^brabsbycategory/(?P<category_id>[a-zA-Z0-9-]+)/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="user-brab-list-view"
    ),
    url(r'^brabsbytag/(?P<tag_name>[a-zA-Z0-9-_  ]+)/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="user-brab-list-view"
    ),
    url(r'^searchbrabs/$', BrabListView.as_view(
        paginate_by=20,
        context_object_name="brab_list"),
        name="search-brab-list-view"
    ),
    url(r'^$', ListView.as_view(
        queryset=Brab.objects.filter(deleted=0),
        paginate_by=20,
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
    url(r'^editbrab/(?P<pk>[a-zA-Z0-9-]+)/$', BrabEditView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab"),
        name="editbrab"
    ),
    url(r'^deletebrab/(?P<pk>[a-zA-Z0-9-]+)/$', BrabEditView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab"),
        name="deletebrab"
    ),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'brabs/brab_list.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('registration.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^user_media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
