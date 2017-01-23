from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError

from leaderboard.models import Competition, Team, Submission, Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


class TeamForm(forms.ModelForm):
    def clean_members(self):
        team = self.instance
        members = [m.id for m in self.cleaned_data.get('members', [])]
        competition = self.cleaned_data.get('competition')
        user_ids = set()
        for t in competition.team_set.all():
            if team.id != t.id:
                for m in t.members.all():
                    user_ids.add(m.id)
        for m in members:
            if m in user_ids:
                raise ValidationError('A user can only belong to one team per competition')
        return members


class TeamAdmin(admin.ModelAdmin):
    form = TeamForm

admin.site.register(User, ProfileAdmin)
admin.site.register(Competition)
admin.site.register(Team, TeamAdmin)
admin.site.register(Submission)
admin.site.register(Profile)
