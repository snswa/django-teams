from operator import attrgetter

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required

from teams.models import Member, Team


def team_tree(L, parent=None):
    teams = Team.objects.filter(parent=parent).order_by('sort_order', 'name')
    if teams:
        L.append('ul')
        for team in teams:
            L.append('li')
            L.append(team)
            team_tree(L, team)
            L.append('/li')
        L.append('/ul')
    return L


@login_required
def index(request, template_name='teams/index.html', extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    L = []
    template_context = {
        'team_tree': team_tree(L),
        'public_teams': Team.objects.filter(is_private=False),
        'private_teams': Team.objects.filter(is_private=True),
    }
    template_context.update(extra_context)
    return render_to_response(
        template_name, template_context, RequestContext(request))


@login_required
def team(request, slug, template_name='teams/team.html', extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    team = get_object_or_404(Team, slug=slug)
    if not request.user.has_perm('teams.view', team):
        raise PermissionDenied()
    request.group = team    # So template context processors can access it.
    template_context = {
        'group': team,
    }
    template_context.update(extra_context)
    return render_to_response(
        template_name, template_context, RequestContext(request))


@login_required
def change_memberships(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        for team in Team.objects.all():
            team_tag = 'team_{0}'.format(team.id)
            user_is_member = user in team.members.all()
            # Add to teams requested but not yet member of, as long as team
            # is not private.
            if team_tag in request.POST and not user_is_member and user.has_perm('teams.join', team):
                Member(team=team, user=user).save()
            # Remove from teams not referenced in POST (because they were not checked in the UI).
            if (team_tag not in request.POST
                and user_is_member
                ):
                Member.objects.get(team=team, user=user).delete()
    redirect_to = reverse('teams_index')
    return HttpResponseRedirect(redirect_to)


@login_required
def team_members(request, slug, template_name='teams/members.html', extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    team = get_object_or_404(Team, slug=slug)
    if not request.user.has_perm('teams.view', team):
        raise PermissionDenied()
    request.group = team    # So template context processors can access it.
    template_context = {
        'group': team,
        'coordinator_list': team.member_set.filter(is_coordinator=True),
        'member_list': team.member_set.all(),
    }
    template_context.update(extra_context)
    return render_to_response(
        template_name, template_context, RequestContext(request))


# @@@ needs test
@login_required
def team_change_membership(request, slug, *args, **kwargs):
    team = get_object_or_404(Team, slug=slug)
    user = request.user
    if request.method == 'POST':
        if request.POST.get('join') and user.has_perm('teams.join', team):
            Member(team=team, user=request.user).save()
        elif request.POST.get('leave'):
            Member.objects.filter(team=team, user=request.user).delete()
    redirect_to = reverse('teams_team_index', kwargs={'slug': slug})
    return HttpResponseRedirect(redirect_to)
