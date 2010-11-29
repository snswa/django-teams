from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext


from teams.models import Team


@login_required
def index(request):
    template_name = 'teams/index.html'
    # @@@ How to do this using queryset only?
    teams = set(Team.objects.filter(is_private=False))
    teams.update(request.user.team_set.all())
    teams = sorted(teams, key=attrgetter('name'))
    template_context = {
        'teams': teams,
    }
    return render_to_response(
        template_name, template_context, RequestContext(request))


@login_required
def team(request, slug):
    template_name = 'teams/team.html'
    team = get_object_or_404(Team, slug=slug)
    template_context = {
        'group': team,
        'is_team_member': team.user_is_member(request.user),
    }
    return render_to_response(
        template_name, template_context, RequestContext(request))
