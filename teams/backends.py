from teams.models import Member, Team


class TeamMembershipBackend(object):

    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        #
        if isinstance(obj, Team):
            if perm == 'teams.ismember':
                return obj.user_is_member(user_obj)
            if perm == 'teams.iscoordinator':
                try:
                    member = Member.objects.get(team=team, user=user)
                except Member.DoesNotExist:
                    return False
                return member.is_coordinator
            if perm == 'teams.view':
                # To view a team, it must be a non-private team, or the
                # user must be a member of the team.
                return obj.user_is_member(user_obj) or not obj.is_private
            if perm == 'teams.join':
                return not obj.user_is_member(user_obj) and not obj.is_private
