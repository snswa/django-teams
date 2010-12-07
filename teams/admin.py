from django.contrib import admin

from inline_ordering.admin import OrderableStackedInline, OrderableTabularInline

from teams.models import Grouping, Member, Team, TeamGrouping


class MemberInline(admin.TabularInline):

    model = Member
    extra = 1


class TeamGroupingInline(OrderableTabularInline):

    model = TeamGrouping
    extra = 1


class GroupingAdmin(admin.ModelAdmin):

    inlines = [
        TeamGroupingInline,
    ]


class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_private', 'auto_join')
    list_filter = ('is_private', 'auto_join')

    inlines = [
        MemberInline,
    ]


admin.site.register(Grouping, GroupingAdmin)
admin.site.register(Team, TeamAdmin)
