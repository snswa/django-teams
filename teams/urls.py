from django.conf.urls.defaults import patterns, url

from teams import views


urlpatterns = patterns(
    'teams.views',
    url(
        regex=r'^$',
        view=views.index,
        name='teams_index',
    ),
    url(
        regex=r'^\$membership/$',
        view=views.change_memberships,
        name='teams_change_memberships',
    ),
    url(
        regex=r'^(?P<slug>[\w\._-]+)/$',
        view=views.team,
        name='teams_team_index',
    ),
    url(
        regex=r'^(?P<slug>[\w\._-]+)/members/$',
        view=views.team_members,
        name='teams_team_members',
    ),
    url(
        regex=r'^(?P<slug>[\w\._-]+)/change_membership/$',
        view=views.team_change_membership,
        name='teams_team_change_membership',
    ),
)
