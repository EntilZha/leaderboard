from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.transaction import atomic
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth

from leaderboard.models import ProfileForm


def index(request):
    return render(request, 'leaderboard/index.html')


@atomic
def register(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'leaderboard/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
