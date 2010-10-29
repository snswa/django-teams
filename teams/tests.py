"""Tests for django-teams"""

from django.contrib.auth.models import User
from django.test import TestCase

from teams.api import user_has_team_role
from teams.models import Role, RoleMembership, Team


class BaseTest(TestCase):

    def setUp(self):
        self.createTestRoles()
        self.createTestTeams()
        self.createTestUser()

    def get(self, node):
        return Team.objects.get(pk=node.id)

    def team(self, fullslug):
        return Team.objects.get(fullslug=fullslug)

    def createTestRoles(self):
        self.manager = Role.objects.create(
            name='manager',
            include_superteams=False,
            include_subteams=True,
        )
        self.member = Role.objects.create(
            name='member',
            include_superteams=True,
            include_subteams=True,
        )
        self.special = Role.objects.create(
            name='special',
            include_superteams=False,
            include_subteams=False,
        )

    def createTestTeams(self):
        self.a = Team.add_root(name='A', slug='a')
        self.b = Team.add_root(name='B', slug='b')
        self.aa = self.get(self.a).add_child(name='AA', slug='a')
        self.ab = self.get(self.a).add_child(name='AB', slug='b')
        self.aaa = self.get(self.aa).add_child(name='AAA', slug='a')
        self.aba = self.get(self.ab).add_child(name='ABA', slug='a')
        self.ba = self.get(self.b).add_child(name='BA', slug='a')

    def createTestUser(self):
        self.user = User.objects.create(username='user1')


class TeamsTest(BaseTest):

    def test_fullslug_shows_dotted_hierarchy_of_slugs(self):
        self.assertEqual('a', self.get(self.a).fullslug)
        self.assertEqual('b', self.get(self.b).fullslug)
        self.assertEqual('a.a', self.get(self.aa).fullslug)
        self.assertEqual('a.b', self.get(self.ab).fullslug)
        self.assertEqual('a.a.a', self.get(self.aaa).fullslug)
        self.assertEqual('a.b.a', self.get(self.aba).fullslug)
        self.assertEqual('b', self.get(self.b).fullslug)

    def test_retrieve_team_by_fullslug(self):
        self.assertEqual(self.a, Team.objects.get(fullslug='a'))
        self.assertEqual(self.b, Team.objects.get(fullslug='b'))
        self.assertEqual(self.aa, Team.objects.get(fullslug='a.a'))
        self.assertEqual(self.ab, Team.objects.get(fullslug='a.b'))
        self.assertEqual(self.aaa, Team.objects.get(fullslug='a.a.a'))
        self.assertEqual(self.aba, Team.objects.get(fullslug='a.b.a'))
        self.assertEqual(self.b, Team.objects.get(fullslug='b'))


class RolesTest(BaseTest):

    def _test_roles(self, role, yes_teams, no_teams):
        for team in yes_teams:
            self.assertTrue(
                user_has_team_role(self.user, team, role),
                'User should have role %r on team %r' % (role, team),
                )
        for team in no_teams:
            self.assertFalse(
                user_has_team_role(self.user, team, role),
                'User should NOT have role %r on team %r' % (role, team),
                )

    def test_special_role(self):
        # Only a single team, no ancestors or descendants.
        RoleMembership.objects.create(
            user=self.user,
            team=self.team('a.a'),
            role=self.special,
        )
        self._test_roles(
            role='special',
            yes_teams=['a.a'],
            no_teams=['a', 'b', 'a.b', 'a.a.a', 'a.b.a', 'b.a'],
        )

    def test_member_role(self):
        # Team, ancestors, and descendants.
        RoleMembership.objects.create(
            user=self.user,
            team=self.team('a.a'),
            role=self.member,
        )
        self._test_roles(
            role='member',
            yes_teams=['a', 'a.a', 'a.a.a'],
            no_teams=['b', 'a.b', 'a.b.a', 'b.a'],
        )

    def test_manager_role(self):
        # Team and descendants.
        RoleMembership.objects.create(
            user=self.user,
            team=self.team('a.a'),
            role=self.manager,
        )
        self._test_roles(
            role='manager',
            yes_teams=['a.a', 'a.a.a'],
            no_teams=['a', 'b', 'a.b', 'a.b.a', 'b.a'],
        )
