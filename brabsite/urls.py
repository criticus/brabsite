from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from brabs.views import BrabDetailView
from brabs.models import Brab
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brabs_list"),
        name="home"
    ),
    url(r'^brab/(?P<pk>[a-zA-Z0-9-]+)/$', BrabDetailView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab"),
        name="brab"
    ),
    url(r'^admin/', include(admin.site.urls)),
)
