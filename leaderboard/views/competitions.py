from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_competitions(request):

    return render(request, 'leaderboard/user_competitions.html')
