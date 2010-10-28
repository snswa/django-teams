from django.db import models as m

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

    def save(self, *args, **kwargs):
        # Build fullslug if not specified.
        if self.fullslug == '':
            teams = list(self.get_ancestors())
            teams.append(self)
            self.fullslug = '.'.join(team.slug for team in teams)
        super(Team, self).save(*args, **kwargs)
