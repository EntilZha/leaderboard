from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from leaderboard.models import Competition, Team, Submission, Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.register(User, ProfileAdmin)
admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(Profile)
