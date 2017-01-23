import importlib

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.dispatch import receiver

from pytz import timezone


COMPETITION_LEVELS = (('novice', 'novice'), ('expert', 'expert'))

SCORING_CLASSES = [('scoring.DefaultScoring', 'scoring.DefaultScoring')]


def get_class(instance_module_class: str):
    instance_module, instance_class = instance_module_class.rsplit('.')
    py_instance_module = importlib.import_module(instance_module)
    py_instance_class = getattr(py_instance_module, instance_class)
    return py_instance_class


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(min_length=1)
    last_name = forms.CharField(min_length=1)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class Profile(models.Model):
    student_id = models.IntegerField(null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'Profile(username={}, student_id={})'.format(self.user.username, self.student_id)


class ProfileForm(forms.ModelForm):
    student_id = forms.IntegerField()

    class Meta:
        model = Profile
        fields = ('student_id',)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Competition(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    level = models.CharField(max_length=20, choices=COMPETITION_LEVELS)
    scoring_class = models.CharField(
        max_length=100, choices=SCORING_CLASSES, default='scoring.DefaultScoring')

    def __str__(self):
        mst = timezone('America/Denver')
        start = self.start_date.astimezone(mst)
        end = self.end_date.astimezone(mst)
        return 'Competition(name={}, level={}, start={:%b %d %Y %I%p} MST, end={:%b %d %Y %I%p} ' \
               'MST)'.format(self.name, self.level, start, end)

    def leaderboard_submissions(self, public=True):
        py_score_class = get_class(self.scoring_class)
        score_inst = py_score_class()
        teams = self.team_set.all()
        paired_scores = []
        no_submission_teams = []
        for t in teams:
            if public:
                if t.leaderboard_submission is None:
                    no_submission_teams.append(t)
                else:
                    paired_scores.append((t.leaderboard_submission.public_score, t))
            else:
                if t.best_private_submission is None:
                    no_submission_teams.append(t)
                else:
                    paired_scores.append((t.best_private_submission.private_score, t))

        sorted_scores = sorted(paired_scores, reverse=score_inst.higher_better)

        return sorted_scores, no_submission_teams


class Team(models.Model):
    name = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    selected_submission = models.ForeignKey(
        'Submission', null=True, related_name='+', blank=True)
    best_public_submission = models.ForeignKey(
        'Submission', null=True, related_name='+', blank=True)
    best_private_submission = models.ForeignKey(
        'Submission', null=True, related_name='+', blank=True)

    @property
    def leaderboard_submission(self):
        if self.selected_submission is not None:
            return self.selected_submission
        else:
            return self.best_public_submission

    def __str__(self):
        competition_name = self.competition.name if self.competition_id is not None else None
        if competition_name is None:
            members = []
        else:
            members = self.members.all()
        return 'Team(name={}, competition={}, members=[{}])'.format(
            self.name,
            competition_name,
            ','.join([m.username for m in members])
        )


class Submission(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    public_score = models.FloatField()
    private_score = models.FloatField()
    submission_time = models.DateTimeField()
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Submission(competition={}, team={}, name={}, public_score={})'.format(
            self.competition.name, self.team.name, self.name, self.public_score)


class NewSubmissionForm(forms.Form):
    competition = forms.IntegerField()
    team = forms.IntegerField()
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}
    ))
    submission_file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(NewSubmissionForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(NewSubmissionForm, self).clean()
        user_team = self.request.user.team_set.filter(id=self.team).first()
        if user_team is None:
            raise forms.ValidationError('Submitting for a team you are not on is not allowed!')
        if self.competition != user_team.competition.id:
            raise forms.ValidationError(
                'The team you are submitting for is not part of this competition')
        print('validating...')
        print(self.cleaned_data['submission_file'])
        return self.cleaned_data

