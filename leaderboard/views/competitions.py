from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def teams(request):
    user = request.user
    user_teams = user.team_set.prefetch_related()
    return render(request, 'leaderboard/user/teams.html', {'teams': user_teams})
