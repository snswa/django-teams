from django import template

from teams.models import Member, Team


register = template.Library()


@register.filter
def iscoordinatorofteam(user, team):
    """Filter to determine if user is a coordinator of a team.

    Example usage::

        {% if user|iscoordinatorofteam:team %}
            You are a coordinator.
        {% else %}
            You are not a coordinator.
        {% endif %}
    """
    if team is None:
        return False
    try:
        member = Member.objects.get(team=team, user=user)
    except Member.DoesNotExist:
        return False
    return member.is_coordinator


@register.filter
def coordinatormembers(team_members):
    """Queryset filter to extract coordinator users from a team member set.

    Example usage::

        {% for member in team.member_set|coordinatorusers %}
            {{ member.user.get_profile }} is a coordinator of {{ team }}.
        {% endfor %}
    """
    return team_members.filter(is_coordinator=True)


@register.filter
def teamforslug(slug):
    """Return the team associated with the given slug.

    Example usage::

        {% with request.GET.team as team_slug %}
            {% if team_slug %}
                {% with team_slug|teamforslug as team %}
                    {{ team.name }}
                {% endwith %}
            {% endif %}
        {% endwith %}
    """
    return Team.objects.get(slug=slug)
