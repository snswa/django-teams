from django.contrib import admin

from teams.models import Member, Team


# -- inlines --


class MemberInline(admin.TabularInline):

    model = Member
    extra = 1


# -- admins --


class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'parent', 'is_private', 'auto_join')
    list_filter = ('is_private', 'auto_join')

    inlines = [
        MemberInline,
    ]


# -- registration --


admin.site.register(Team, TeamAdmin)
