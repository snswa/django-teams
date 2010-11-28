from django.contrib import admin

from teams.models import Team


class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_private', 'auto_join')
    list_filter = ('is_private', 'auto_join')


admin.site.register(Team, TeamAdmin)
