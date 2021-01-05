from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
  url(r'^$', views.currentstatus, name='currentstatus'),
  url(r'^main$', views.main, name='main'),
  url(r'^details$', views.main_details, name='main_details'),
  url(r'^stats$', views.stats, name='stats'),
  url(r'^pumpstatus$', views.pumpstatus, name='pumpstatus'),
] 


