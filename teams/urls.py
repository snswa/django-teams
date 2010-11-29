from django.conf.urls.defaults import patterns, url

from teams import views


urlpatterns = patterns(
    'teams.views',
    url(r'^$', views.index, name='teams_index'),
    url(r'^(?P<slug>[\w\._-]+)/$', views.team, name='teams_team'),
)
