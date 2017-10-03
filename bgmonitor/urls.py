from django.conf.urls import url
from . import views


urlpatterns = [
  url(r'^$', views.main, name='main'),
  url(r'^details$', views.main_details, name='main_details'),
  url(r'^stats$', views.stats, name='stats'),
]

