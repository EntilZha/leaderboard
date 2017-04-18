from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm

from leaderboard.views import users
from leaderboard.views import competitions

urlpatterns = [
    url(r'^register/$', users.register, name='register'),
    url(r'^login/$', login, {
        'template_name': 'register.html',
        'authentication_form': AuthenticationForm
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^user/teams/$', competitions.teams),
    url(r'^user/profile/(?P<username>[\w.@+-]+)/$', users.profile),
    url(r'^competition/$', competitions.CompetitionListView.as_view(), name='competition_list'),
    url(r'^competition/(?P<competition_name>[a-zA-Z ]+)/$', competitions.competition),
    url(r'^competition/(?P<competition_name>[a-zA-Z ]+)/submit/$', competitions.new_submission)
]
