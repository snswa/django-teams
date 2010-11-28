from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Team(models.Model):

    slug = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    auto_join = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def user_is_member(self, user):
        return (Member.objects.filter(team=self, user=user).count() == 1)


class Member(models.Model):

    user = models.ForeignKey(User, related_name='team_members')
    team = models.ForeignKey(Team, related_name='members')
    is_coordinator = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        rel = 'coordinator' if self.is_coordinator else 'member'
        return u'{0}, {1} of {2}'.format(self.user, rel, self.team)


def auto_join_user_with_no_memberships(sender, instance=None, **kwargs):
    if instance is not None:
        membership_count = Member.objects.filter(user=instance).count()
        if membership_count == 0:
            for team in Team.objects.filter(is_private=False, auto_join=True):
                Member.objects.create(user=instance, team=team)

post_save.connect(auto_join_user_with_no_memberships, sender=User)
