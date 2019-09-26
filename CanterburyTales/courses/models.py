from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from CanterburyTales.profiles.models import Profile


class Tag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title


class Audience(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100, blank=False)
    year_written = models.IntegerField(default=timezone.now().year)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    posted = models.DateField(null=True, )
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    audience = models.ManyToManyField(Audience)
    lesson_length = models.IntegerField(null=True)
    upvotes = models.ManyToManyField(Profile, related_name='upvotes', default=0)
    views = models.IntegerField(default=0)



