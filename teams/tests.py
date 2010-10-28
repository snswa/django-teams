"""Tests for django-teams"""

from django.contrib.auth.models import User
from django.test import TestCase

from teams.models import Team


class TeamsTest(TestCase):

    def get(self, node):
        return Team.objects.get(pk=node.id)

    def team(self, fullslug):
        return Team.objects.get(fullslug=fullslug)

    def setUp(self):
        self.createTestTeams()
        self.createTestUser()

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

    def test_user_is_member_of_team(self):
        a = self.team('a')
        a.members.add(self.user)
        a.save()
        self.assertTrue(a.has_member(self.user))
        self.assertFalse(a.has_manager(self.user))

    def test_user_is_manager_of_team(self):
        a = self.team('a')
        a.members.add(self.user)
        a.managers.add(self.user)
        a.save()
        self.assertTrue(a.has_member(self.user))
        self.assertTrue(a.has_manager(self.user))

    def test_user_is_manager_of_team_and_automatically_a_member(self):
        a = self.team('a')
        a.managers.add(self.user)
        a.save()
        self.assertTrue(a.has_member(self.user))
        self.assertTrue(a.has_manager(self.user))

    def test_user_removed_from_team_no_longer_manager(self):
        a = self.team('a')
        a.managers.add(self.user)
        a.save()
        self.assertTrue(a.has_member(self.user))
        self.assertTrue(a.has_manager(self.user))
        a.members.remove(self.user)
        a.save()
        self.assertFalse(a.has_member(self.user))
        self.assertFalse(a.has_manager(self.user))

    def test_member_is_defacto_member_of_team(self):
        aa = self.team('a.a')
        aa.members.add(self.user)
        aa.save()
        self.assertTrue(aa.has_defacto_member(self.user))
        aa.members.remove(self.user)
        aa.save()
        self.assertFalse(aa.has_defacto_member(self.user))

    def _test_defacto(self, type, member_of, not_member_of):
        method_name = 'has_defacto_%s' % type
        for fullslug in member_of:
            fn = getattr(self.team(fullslug), method_name)
            self.assertTrue(
                fn(self.user),
                'Should be %s of %r but is not' % (type, fullslug),
                )
        for fullslug in not_member_of:
            fn = getattr(self.team(fullslug), method_name)
            self.assertFalse(
                fn(self.user),
                'Should not be %s of %r but is' % (type, fullslug),
                )

    def test_member_is_defacto_member_of_direct_ancestors(self):
        t = self.team('a.b.a')
        t.members.add(self.user)
        t.save()
        self._test_defacto(
            'member',
            member_of=['a.b.a', 'a.b', 'a'],
            not_member_of=['a.a', 'a.a.a', 'b', 'b.a'],
        )

    def test_member_is_defacto_member_of_all_descendants(self):
        t = self.team('a')
        t.members.add(self.user)
        t.save()
        self._test_defacto(
            'member',
            member_of=['a', 'a.a', 'a.b', 'a.a.a', 'a.b.a'],
            not_member_of=['b', 'b.a'],
        )

    def test_member_is_not_defacto_member_of_descendants_of_direct_ancestors(self):
        t = self.team('a.b')
        t.members.add(self.user)
        t.save()
        self._test_defacto(
            'member',
            member_of=['a', 'a.b', 'a.b.a'],
            not_member_of=['a.a', 'a.a.a', 'b', 'b.a'],
        )

    def test_manager_is_defacto_manager_of_team(self):
        aa = self.team('a.a')
        aa.managers.add(self.user)
        aa.save()
        self.assertTrue(aa.has_defacto_manager(self.user))
        aa.managers.remove(self.user)
        aa.save()
        self.assertFalse(aa.has_defacto_manager(self.user))

    def test_manager_is_defacto_manager_of_all_descendants(self):
        t = self.team('a.b')
        t.managers.add(self.user)
        t.save()
        self._test_defacto(
            'manager',
            member_of=['a.b', 'a.b.a'],
            not_member_of=['a', 'a.a', 'a.a.a', 'b', 'b.a'],
        )

    def test_manager_is_not_defacto_manager_of_ancestors(self):
        t = self.team('a.b.a')
        t.managers.add(self.user)
        t.save()
        self._test_defacto(
            'manager',
            member_of=['a.b.a'],
            not_member_of=['a', 'a.a', 'a.a.a', 'a.b', 'b', 'b.a'],
        )
