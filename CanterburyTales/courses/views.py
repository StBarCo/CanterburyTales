from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import  loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from .forms import CourseForm
import datetime
from .models import Course, Profile, User, Tag, CourseFile
import zipfile
import os
from django.db.models import Count


class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    queryset = Course.objects \
        .annotate(num_upvotes=Count('upvotes')) \
        .order_by('-num_upvotes','-views')


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
