"""Tests for django-teams"""

from django.contrib.auth.models import User
from django.test import TestCase

from teams.models import Team, Member


class TestTeams(TestCase):

    def test_auto_join(self):
        team_auto = Team.objects.create(slug='auto', name='Auto Join', auto_join=True)
        team_noauto = Team.objects.create(slug='noauto', name='No Auto Join')
        user1 = User.objects.create(username='user1')
        assert team_auto.user_is_member(user1)
        assert not team_noauto.user_is_member(user1)

    def test_private_no_auto_join(self):
        team_auto = Team.objects.create(slug='auto', name='Auto Join', auto_join=True, is_private=True)
        team_noauto = Team.objects.create(slug='noauto', name='No Auto Join', is_private=True)
        user1 = User.objects.create(username='user1')
        assert not team_auto.user_is_member(user1)
        assert not team_noauto.user_is_member(user1)
