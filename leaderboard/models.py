from django.db import models
from authtools.models import User


COMPETITION_LEVELS = (('novice', 'novice'), ('expert', 'expert'))


class StudentInfo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Competition(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    level = models.CharField(max_length=20, choices=COMPETITION_LEVELS)


class Team(models.Model):
    name = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class Submission(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.FloatField()
    submission_time = models.DateTimeField()
