from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import  loader
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from .forms import CourseForm
import datetime
from .models import Course, Profile, User, Audience, Tag


class IndexView(generic.ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'


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


class CourseCreate(FormView):
    template_name = 'courses/course_form.html'
    form_class = CourseForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # data = form.clean_author()
        course = form.save(commit=False)
        course.author = Profile.objects.all().first()
        course.posted = datetime.date.today()
        course.save()
        form.save_m2m()
        return super().form_valid(form)


class CourseUpdate(UpdateView):
    model = Course
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class CourseDelete(DeleteView):
    model = Course
    # success_url = reverse_lazy('courses')
