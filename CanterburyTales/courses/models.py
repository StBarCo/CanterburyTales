from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from CanterburyTales.profiles.models import Profile
from django.contrib.postgres.fields import IntegerRangeField
import os
import math
import datetime


class Tag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/courses/username/datetime/<filename>
    user_n = instance.course.author.user.username
    course_title = ''.join(e for e in instance.course.title[:15] if e.isalnum())

    return os.path.join('courses', user_n, course_title, filename)


class Course(models.Model):
    title = models.CharField(max_length=100, blank=False)
    year_written = models.IntegerField(default=timezone.now().year)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    posted = models.DateField(null=True, )
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    audience = IntegerRangeField()
    count = models.IntegerField(default=1)
    duration = models.DurationField(null=True, default=30)
    upvotes = models.ManyToManyField(Profile, related_name='upvotes', blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title

    def audience_description(self):
        return Audience().get_description(self.audience.lower, self.audience.upper)

    def views_humanized(self):
        return humanized_count(self.views)

    def posted_humanized(self):
        return humanized_duration(datetime.date.today(), self.posted)

    def add_view(self):
        self.views = self.views + 1
        self.save()



def humanized_count(i):
    if i <= 10:
        return str(i)
    elif i <= 200:
        return str(math.floor(i / 10) * 10) + '+'
    elif i <= 1000:
        return str(math.floor(i / 100) * 100) + '+'
    elif i <= 10000:
        return str(math.floor(i / 1000) * 1000) + '+'
    elif i <= 100000:
        return str(math.floor(i / 10000) * 10000) + '+'
    elif i <= 1000000:
        return str(math.floor(i / 100000) * 100000) + '+'
    elif i > 1000000:
        return str(math.floor(i / 1000000)) + ' million +'
    else:
        return str(i)


def humanized_duration(newer_date, older_date):
    days = (newer_date - older_date).days
    if days == 0:
        return 'Today'
    if days == 1:
        return 'Yesterday'
    if days < 30:
        return str(days) + ' days ago'
    elif days < 50:
        return '1 month'
    elif days < 365*2:
        return str(math.floor(days/(365/12))) + ' months ago'
    else:
        return  str(math.floor(days/365)) + ' years ago'


class CourseFile(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Audience:
    def __init__(self):
        self.definitions = {
            0: 'Infant / Toddler',
            3: 'Pre-K',
            5: 'Kindergarten',
            6: '1st Grade',
            7: '2nd Grade',
            8: '3rd Grade',
            9: '4th Grade',
            10: '5th Grade',
            11: '6th Grade',
            12: '7th Grade',
            13: '8th Grade',
            14: '9th Grade',
            15: '10th Grade',
            16: '11th Grade',
            17: '12th Grade',
            18: 'University',
            22: 'Young Adults',
            50: 'Mid-life',
            65: 'Retired',
        }

        self.special = {
            "0,10": 'Children (Infant-5th Grade)',
            "11,13": 'Middle School',
            '14,17': 'High School',
            '11,17': 'Youth (Middle and High School)',
            '18,65': 'Adults (18-65)',
            '0,18': 'Children and Youth',
            '0,65': 'Everyone'
        }

    def get_title(self, age):
        return self.definitions.get(age)

    def get_range_titles(self, bounds):
        # if bounds is in special definitions, use that,
        # otherwise return text "5th Grade through 6th Grade"
        titles = (self.definitions.get(bounds[0]), self.definitions.get(bounds[1]))
        return titles

    def get_definitions(self):
        return self.definitions

    def get_definition(self, n):
        return self.definitions[n]

    def get_special_definitions(self):
        return self.special

    def get_special_definition(self, s):
        if s in self.special:
            return self.special[s]
        return False

    def get_description(self, lower, upper):
        description = self.get_special_definition(str(lower) + ',' + str(upper))
        if not description:
            description = self.get_definition(lower) + ' through ' + self.get_definition(upper)
        return description
