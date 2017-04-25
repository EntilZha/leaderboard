from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic.list ListView
from django.utils import timezone

from leaderboard.models import Competition, NewSubmissionForm, Submission
from scoring.abstract import get_class


class CompetitionListView(ListView):
    model = Competition


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

    user_team = request.user.team_set.filter(competition_id=comp.id).first()
    if request.method == 'GET':
        if user_team is None:
            messages.error(
                request,
                'You are not on a team for this competition yet, contact an admin to join a team')
            return redirect('/')
        form = NewSubmissionForm()
    else:
        form = NewSubmissionForm(
            request.POST,
            request.FILES,
            request=request,
            team_id=user_team.id,
            competition_id=comp.id
        )
        if form.is_valid():
            submission_content = form.cleaned_data['submission_file'].read().decode('utf-8')
            py_score_class = get_class(comp.scoring_class)
            score_inst = py_score_class()
            sub_validation, error = score_inst.validate(submission_content)
            if sub_validation:
                public_score, private_score, error = score_inst.score(submission_content)
                if error is None:
                    submission = Submission(
                        competition_id=comp.id,
                        team_id=user_team.id,
                        public_score=public_score,
                        private_score=private_score,
                        submission_time=timezone.now(),
                        name=form.cleaned_data['name'],
                        description=form.cleaned_data['description']
                    )
                    submission.save()
                    user_team.update_best_submissions(score_inst.higher_better)
                    messages.info(request, 'Submission successful!')
                    return redirect('/competition/{}'.format(competition_name))
                else:
                    messages.error(request, error)
            else:
                messages.error(request, error)
    return render(request, 'leaderboard/competition/submit.html', {'form': form})
