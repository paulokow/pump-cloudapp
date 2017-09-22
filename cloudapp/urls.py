from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^bgmonitor/', include('bgmonitor.urls')),
    url(r'^/$', RedirectView.as_view(url='/bgmonitor')),
    url(r'^admin/', admin.site.urls)
]

