from django.shortcuts import render, redirect
from django.db.transaction import atomic
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

from leaderboard.models import ProfileForm, CustomUserCreationForm


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
            login(request, user)
            messages.success(request, 'Successfully created user and logged you in')
            return redirect('/')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'leaderboard/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def profile(request, username=None):
    if username is None:
        messages.error(request, 'User with username "{}" does not exist'.format(username))
        return redirect('/')
    else:
        user = User.objects.filter(username=username).first()
        if user is None:
            messages.error(request, 'User with username "{}" does not exist'.format(username))
            return redirect('/')
        else:
            return render(request, 'leaderboard/user/profile.html', {'profile_user': user})
