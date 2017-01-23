from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from leaderboard.models import Competition


@login_required
def teams(request):
    user = request.user
    user_teams = user.team_set.prefetch_related()
    return render(request, 'leaderboard/user/teams.html', {'teams': user_teams})


def competition(request, competition_name=None):
    if competition_name is None:
        messages.error(request, 'Competition with name "{}" does not exist'.format(
            competition_name))
        return redirect('/')

    comp = Competition.objects.filter(name__iexact=competition_name).first()
    if comp is None:
        messages.error(request, 'Competition with name "{}" does not exist'.format(
            competition_name))
        return redirect('/')
    else:
        return render(request, 'leaderboard/competition/competition.html', {'competition': comp})
