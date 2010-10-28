from django.db import models as m
from django.db.models.signals import m2m_changed

from treebeard.ns_tree import NS_Node


class Team(NS_Node):
    """A team of users."""

    name = m.CharField(max_length=40)
    slug = m.CharField(max_length=20)
    fullslug = m.CharField(max_length=255, unique=True)
    members = m.ManyToManyField('auth.User', related_name='teams_member_of')
    managers = m.ManyToManyField('auth.User', related_name='teams_manager_of')

    node_order_by = ['slug']

    def __unicode__(self):
        return self.fullslug

    def has_manager(self, user):
        return user.teams_manager_of.filter(pk=self.pk).count() > 0

    def has_defacto_manager(self, user):
        if self.has_manager(user):
            return True
        # Don't have direct managership.  Check user's managerships to
        # determine de facto managership.
        for team in user.teams_manager_of.all():
            # Look to see if self is below this team that the user manages.
            if self.is_descendant_of(team):
                return True
        return False

    def has_member(self, user):
        return user.teams_member_of.filter(pk=self.pk).count() > 0

    def has_defacto_member(self, user):
        if self.has_member(user):
            return True
        #
        # Don't have direct membership.  Check user's memberships to determine
        # de facto membership.
        for team in user.teams_member_of.all():
            # Look to see if self is below this team that the user is a
            # member of.
            if self.is_descendant_of(team):
                return True
            # Look to see if the team the user is a member of is below
            # self.
            if team.is_descendant_of(self):
                return True
        return False

    def save(self, *args, **kwargs):
        # Build fullslug if not specified.
        if self.fullslug == '':
            teams = list(self.get_ancestors())
            teams.append(self)
            self.fullslug = '.'.join(team.slug for team in teams)
        #
        # Continue saving.
        super(Team, self).save(*args, **kwargs)

    @staticmethod
    def on_members_changed(sender, instance, action, model, pk_set, **kwargs):
        if action == 'post_remove':
            team = instance
            # For each member removed, also remove them as a manager if they
            # are a manager.
            leftover_managers = team.managers.filter(pk__in=pk_set)
            team.managers.remove(*leftover_managers.all())

    @staticmethod
    def on_managers_changed(sender, instance, action, model, pk_set, **kwargs):
        if action == 'post_add':
            team = instance
            # For each manager added, also add them as a member if they are
            # not already.
            non_members = team.managers.exclude(teams_member_of__in=[team])
            team.members.add(*non_members.all())


m2m_changed.connect(Team.on_members_changed, sender=Team.members.through)
m2m_changed.connect(Team.on_managers_changed, sender=Team.managers.through)
