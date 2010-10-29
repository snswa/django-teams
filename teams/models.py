from django.db import models as m
from django.db.models.signals import m2m_changed

from treebeard.ns_tree import NS_Node


class RoleMembership(m.Model):
    """A role that users have within a team."""

    user = m.ForeignKey('auth.User')
    role = m.ForeignKey('teams.Role')
    team = m.ForeignKey('teams.Team')

    class Meta:
        unique_together = (
            ('user', 'role', 'team'),
        )

    def __unicode__(self):
        return '%s, %s of %s' % (self.user, self.role, self.team)


class Role(m.Model):
    """A type of role that users can have within a team."""

    name = m.CharField(max_length=20, unique=True)
    include_superteams = m.BooleanField(default=False)
    include_subteams = m.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Team(NS_Node):
    """A team of users."""

    name = m.CharField(max_length=40)
    slug = m.CharField(max_length=20)
    fullslug = m.CharField(max_length=255, unique=True, blank=True)

    node_order_by = ['slug']

    def __unicode__(self):
        return self.fullslug

    def save(self, *args, **kwargs):
        # Always rebuild fullslug when saving.
        teams = list(self.get_ancestors())
        teams.append(self)
        self.fullslug = '.'.join(team.slug for team in teams)
        #
        # Continue saving.
        super(Team, self).save(*args, **kwargs)
