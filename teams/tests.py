"""Tests for django-teams"""

from django.test import TestCase

from teams.models import Team


class TeamsTest(TestCase):

    def get(self, node):
        return Team.objects.get(pk=node.id)

    def setUp(self):
        self.createTestTeams()

    def createTestTeams(self):
        self.a = Team.add_root(name='A', slug='a')
        self.b = Team.add_root(name='B', slug='b')
        self.aa = self.get(self.a).add_child(name='AA', slug='a')
        self.ab = self.get(self.a).add_child(name='AB', slug='b')
        self.aaa = self.get(self.aa).add_child(name='AAA', slug='a')
        self.aba = self.get(self.ab).add_child(name='ABA', slug='a')
        self.ba = self.get(self.b).add_child(name='BA', slug='a')

    def test_fullslug_shows_dotted_hierarchy_of_slugs(self):
        self.assertEqual('a', self.get(self.a).fullslug)
        self.assertEqual('b', self.get(self.b).fullslug)
        self.assertEqual('a.a', self.get(self.aa).fullslug)
        self.assertEqual('a.b', self.get(self.ab).fullslug)
        self.assertEqual('a.a.a', self.get(self.aaa).fullslug)
        self.assertEqual('a.b.a', self.get(self.aba).fullslug)
        self.assertEqual('b', self.get(self.b).fullslug)

    def test_retrieve_team_by_fullslug(self):
        """
        """

    def test_member_is_defacto_member_of_direct_ancestors(self):
        """
        """

    def test_member_is_defacto_member_of_all_descendants(self):
        """
        """

    def test_member_is_not_defacto_member_of_descendants_of_direct_ancestors(self):
        """
        """

    def test_manager_is_defacto_manager_of_all_descendants(self):
        """
        """

    def test_manager_is_not_defacto_manager_of_ancestors(self):
        """
        """
