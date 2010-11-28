from django.contrib import admin

from teams.models import Team, Member


class MemberInline(admin.TabularInline):

    model = Member
    extra = 1


class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_private', 'auto_join')
    list_filter = ('is_private', 'auto_join')

    inlines = [
        MemberInline,
    ]


admin.site.register(Team, TeamAdmin)
