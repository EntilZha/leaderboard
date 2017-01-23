from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_GET, require_http_methods

from leaderboard.models import Competition, NewSubmissionForm


@require_GET
@login_required
def teams(request):
    user = request.user
    user_teams = user.team_set.prefetch_related()
    return render(request, 'leaderboard/user/teams.html', {'teams': user_teams})


@require_GET
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

    paired_scores, no_submission_teams = comp.leaderboard_submissions()
    return render(request, 'leaderboard/competition/competition.html', {
        'competition': comp,
        'paired_scores': paired_scores,
        'no_submission_teams': no_submission_teams
    })


@require_http_methods(['GET', 'POST'])
@login_required
def new_submission(request, competition_name=None):
    if competition_name is None:
        messages.error(request, 'Competition with name "{}" does not exist'.format(
            competition_name))
        return redirect('/')

    comp = Competition.objects.filter(name__iexact=competition_name).first()
    if comp is None:
        messages.error(request, 'Competition with name "{}" does not exist'.format(
            competition_name))
        return redirect('/')

    if request.GET:
        form = NewSubmissionForm()
        form.fields['competition'] = comp.id
        user_team = request.user.team_set.filter(competition_id=comp.id).first()
        if user_team is None:
            messages.error(
                request,
                'You are not on a team for this competition yet, contact an admin to join a team')
            return redirect('/')
        form.fields['team'] = user_team.id
    else:
        form = NewSubmissionForm(request=request)
        print(request)
        if form.is_valid():
            messages.info(request, 'Submission successful!')
            return redirect('/')
        else:
            print(form.fields['competition'])
    return render(request, 'leaderboard/competition/submit.html', {'form': form})
