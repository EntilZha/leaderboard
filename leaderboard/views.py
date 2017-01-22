from django.shortcuts import render, redirect
from django.db.transaction import atomic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

from leaderboard.models import ProfileForm, CustomUserCreationForm


def index(request):
    return render(request, 'leaderboard/index.html')


@atomic
def register(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'leaderboard/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
