from django.db import models as m

from treebeard.ns_tree import NS_Node


class Team(NS_Node):
    """A team of users."""

    name = m.CharField(max_length=40)
    slug = m.CharField(max_length=20)
    members = m.ManyToManyField('auth.User', related_name='teams_member_of')
    managers = m.ManyToManyField('auth.User', related_name='teams_manager_of')
