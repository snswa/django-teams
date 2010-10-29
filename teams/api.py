from teams.models import Role, RoleMembership, Team


def user_has_team_role(user, team, role):
    if isinstance(team, basestring):
        team = Team.objects.get(fullslug=team)
    if isinstance(role, basestring):
        role = Role.objects.get(name=role)
    #
    # Check direct membership.
    memberships = RoleMembership.objects.filter(
        user=user,
        team=team,
        role=role,
    )
    if memberships.count() == 1:
        return True
    #
    # Short-circuit if we're not to check team ancestors and descendants.
    if not (role.include_superteams or role.include_subteams):
        return False
    #
    # Check ancestors and descendants as needed.
    memberships = user.rolemembership_set.filter(
        role=role,
    )
    for membership in memberships.all():
        # Check superteams.
        if role.include_superteams:
            if membership.team.is_descendant_of(team):
                return True
        #
        # Check subteams.
        if role.include_subteams:
            if team.is_descendant_of(membership.team):
                return True
    #
    # No matches.
    return False
