from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.db.utils import DatabaseError

from taggit.managers import TaggableManager

from groups.base import GroupBase


class Grouping(models.Model):
    """A conceptual grouping of teams.  E.g. 'Special Interest' or 'NW Region'"""

    name = models.CharField(max_length=100, unique=True)
    teams = models.ManyToManyField('Team', through='GroupingTeam')
    tags = TaggableManager()

    def __unicode__(self):
        return self.name


class GroupingTeam(models.Model):

    grouping = models.ForeignKey(Grouping)
    team = models.ForeignKey('Team')


class Member(models.Model):
    """A user's membership in a team."""

    user = models.ForeignKey(User)
    team = models.ForeignKey('teams.Team')
    is_coordinator = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        rel = 'coordinator' if self.is_coordinator else 'member'
        return u'{0}, {1} of {2}'.format(self.user, rel, self.team)


class Team(GroupBase):
    """A team, either public or private, that has members."""

    slug = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    auto_join = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='Member')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teams_team', kwargs={'slug': self.slug})


def auto_join_user_with_no_memberships(sender, instance=None, **kwargs):
    if instance is not None:
        try:
            membership_count = Member.objects.filter(user=instance).count()
        except DatabaseError, e:
            # Creating a superuser with syncdb on first run;
            # teams_member table doesn't yet exist.
            if 'no such table: teams_member' in str(e):
                pass
        else:
            if membership_count == 0:
                for team in Team.objects.filter(is_private=False, auto_join=True):
                    Member.objects.create(user=instance, team=team)

post_save.connect(auto_join_user_with_no_memberships, sender=User)
