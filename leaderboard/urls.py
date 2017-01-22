from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm

from leaderboard import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {
        'template_name': 'register.html',
        'authentication_form': AuthenticationForm
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'})
]
