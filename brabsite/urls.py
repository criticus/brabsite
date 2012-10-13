from django.conf.urls import *
from django.contrib import admin
from django.views.generic import ListView, DetailView
from brabs.models import Brab
from brabs.views import BrabDetailView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', ListView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab_list"),
        name="home"
    ),
    url(r'^brab/(?P<pk>[a-zA-Z0-9-]+)/$', BrabDetailView.as_view(
        queryset=Brab.objects.all(),
        context_object_name="brab"),
        name="brab"
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
)
