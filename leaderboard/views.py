from django.http import HttpResponseRedirect
from django.shortcuts import render
from authtools.forms import UserCreationForm


def index(request):
    return render(request, 'leaderboard/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # do stuff
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'leaderboard/register.html', {'form': form})
