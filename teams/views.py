from operator import attrgetter

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required


from teams.models import Member, Team


@login_required
def index(request):
    template_name = 'teams/index.html'
    template_context = {
        'public_teams': Team.objects.filter(is_private=False),
        'private_teams': Team.objects.filter(is_private=True),
    }
    return render_to_response(
        template_name, template_context, RequestContext(request))


@login_required
def team(request, slug):
    template_name = 'teams/team.html'
    team = get_object_or_404(Team, slug=slug)
    request.group = team    # So template context processors can access it.
    template_context = {
        'group': team,
        'is_team_member': team.user_is_member(request.user),
    }
    return render_to_response(
        template_name, template_context, RequestContext(request))


# @@@ needs test
@login_required
def membership(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if request.method == 'POST':
        if request.POST.get('join'):
            print 'joining'
            if not team.is_private and not request.user in team.members.all():
                Member(team=team, user=request.user).save()
        elif request.POST.get('leave'):
            Member.objects.filter(team=team, user=request.user).delete()
    redirect_to = reverse('teams_team', kwargs={'slug': slug})
    return HttpResponseRedirect(redirect_to)
