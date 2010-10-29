from django.contrib import admin

from treebeard.admin import TreeAdmin

from teams.models import Role, RoleMembership, Team


class MembershipInline(admin.TabularInline):

    model = RoleMembership


class TeamAdmin(TreeAdmin):

    inlines = [
        MembershipInline,
    ]


admin.site.register(Role)
admin.site.register(Team, TeamAdmin)
