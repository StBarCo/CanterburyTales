from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from .forms import CourseForm, FilterForm
import datetime
from .models import Course, Profile, User, Tag, CourseFile, Audience
import zipfile
import os
from django.db.models import Count
from psycopg2.extras import Range, NumericRange
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.TemplateView):
    # template_name = 'courses/index.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return 'courses/course_list.html'
        return 'courses/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_params'] = {
            'audience': parse_audience_params(self.kwargs.get('audience', '0,65')),
            'audience_exact': bool(self.kwargs.get('audience_exact', 0)),
            'tags': parse_tag_params(self.kwargs.get('tags', '')),
            'tags_exact': bool(self.kwargs.get('tags_exact', 0)),
        }
        context['courses'] = self.get_queryset(context['search_params'])
        context['form'] = FilterForm(initial={
            'audience_0': context['search_params']['audience'][0],
            'audience_1': context['search_params']['audience'][1],
            'audience_exact': context['search_params']['audience_exact'],
            'tags': context['search_params']['tags'],
            'tags_exact': context['search_params']['tags_exact'],
        }
        )
        return context

    def get_queryset(self, params):
        queryset = filter_audience(params['audience'], params['audience_exact'])
        queryset = filter_tags(queryset, params['tags'], params['tags_exact'])

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


class CourseCreate(LoginRequiredMixin, FormView):
    template_name = 'courses/course_form.html'
    form_class = CourseForm
    success_url = '/'
    login_url = 'login'

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


def parse_audience_params(string):
    audience_defs = Audience().get_definitions().keys()
    a_range = string.split('-')

    if not len(a_range) == 2:
        return [0, 65]
    elif not (a_range[0].isdigit() & a_range[1].isdigit()):
        return [0, 65]
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
    return a_range


def filter_audience(audience, match_type):
    if match_type:
        return Course.objects.filter(audience__startswith=audience[0]).filter(audience__endswith=audience[1])
    else:
        return Course.objects.filter(audience__overlap=NumericRange(audience[0], audience[1]))


def parse_tag_params(string):
    tags = []
    if string == '' or string == 'all':
        return ''

    for tag in string.split('&'):
        if tag.isdigit():
            tags.append(tag)
            tags_set = Tag.objects.filter(id__in=tags)
        else:
            tags.append(tag.title())
            tags_set = Tag.objects.filter(title__in=tags)

    return tags_set.values_list('id', flat=True)


def filter_tags(queryset, tags, match_type):
    if tags == '':
        return queryset
    if match_type:
        for tag in tags:
            queryset = queryset.filter(tags=tag)
        return queryset
    else:
        return queryset.filter(tags__in=tags)
