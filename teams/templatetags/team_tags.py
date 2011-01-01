from django import template

from teams.models import Member


register = template.Library()


@register.filter
def iscoordinatorofteam(user, team):
    """Filter to determine if user is a coordinator of a team.

    Example usage::

        {% load team_tags %}
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
