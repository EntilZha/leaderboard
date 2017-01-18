from django.contrib import admin
from leaderboard.models import Competition, Team, Submission, StudentInfo


admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(StudentInfo)
