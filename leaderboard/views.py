from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.transaction import atomic
from authtools.forms import UserCreationForm

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
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'leaderboard/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
