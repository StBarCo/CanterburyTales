from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from .forms import CourseForm
import datetime
from .models import Course, Profile, User, Tag, CourseFile, Audience
import zipfile
import os
from django.db.models import Count
from psycopg2.extras import Range, NumericRange
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models


class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = parse_age_params(self.kwargs.get('age', 'all'), self.kwargs.get('age_exact', 0))
        queryset = parse_tag_params(queryset, self.kwargs.get('tags', 'all'), self.kwargs.get('tags_exact', 0))

        queryset = queryset.annotate(num_upvotes=Count('upvotes')) \
            .order_by('-num_upvotes', '-views')
        return queryset


class DetailView(generic.DetailView):
    model = Course
    template_name = 'courses/detail.html'
    fields = [
        'title',
        'year_written',
        'tags',
        'audience',
        'lesson_length',
        'description',
    ]

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        obj.add_view()
        return context


class CourseCreate(FormView):
    template_name = 'courses/course_form.html'
    form_class = CourseForm
    success_url = '/'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.author = Profile.objects.all().first()
        course.posted = datetime.date.today()
        course.save()
        form.save_m2m()
        for f in form.files.getlist('course_files'):
            CourseFile.objects.create(file=f, course=course)

        return super().form_valid(form)


class CourseUpdate(UpdateView):
    model = Course
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class CourseDelete(DeleteView):
    model = Course
    # success_url = reverse_lazy('courses')


def course_upvote(request, pk):
    course = Course.objects.get(pk=pk)
    profile = request.user.profile
    course.upvotes.add(request.user.profile)
    course.save()
    return HttpResponseRedirect(reverse('courses:index'))


def parse_age_params(string, match_type):
    audience_defs = Audience().get_definitions().keys()
    a_range = string.split('-')

    if not len(a_range) == 2:
        return Course.objects.all()
    elif not (a_range[0].isdigit() & a_range[1].isdigit()):
        return Course.objects.all()
    elif a_range == [0, 65]:
        return Course.objects.all()
    else:
        temp_list = []
        for i in a_range:
            val = int(i)
            if val not in audience_defs:
                temp_i = 0
                for age in audience_defs:
                    if age <= val:
                        temp_i = age
                    else:
                        break
                temp_list.append(temp_i)
            else:
                temp_list.append(val)
        a_range = temp_list

    if match_type:
        return Course.objects.filter(audience__startswith=a_range[0]).filter(audience__endswith=a_range[1])
    else:
        return Course.objects.filter(audience__overlap=NumericRange(a_range[0], a_range[1]))


def parse_tag_params(queryset, string, match_type):
    tags = []
    if string == 'all':
        return queryset

    for tag in string.split('&'):
        if tag.isdigit():
            tags.append(tag)
            tags_set = Tag.objects.filter(id__in=tags)
        else:
            tags.append(tag.title())
            tags_set = Tag.objects.filter(title__in=tags)

    if match_type:
        for tag in tags_set:
            queryset = queryset.filter(tags=tag)
        return queryset
    else:
        return queryset.filter(tags__in=tags_set)
