from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django import forms
from django.dispatch import receiver


COMPETITION_LEVELS = (('novice', 'novice'), ('expert', 'expert'))


class Profile(models.Model):
    student_id = models.IntegerField(null=True, unique=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class ProfileForm(forms.ModelForm):
    email = models.EmailField(unique=True)
    student_id = models.IntegerField(unique=True)

    class Meta:
        model = Profile
        fields = ('email', 'student_id')


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


class Team(models.Model):
    name = models.CharField(max_length=50)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class Submission(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.FloatField()
    submission_time = models.DateTimeField()
