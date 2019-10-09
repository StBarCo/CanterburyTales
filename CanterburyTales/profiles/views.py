from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ProfileForm
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('courses:index')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'profile/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


class DetailView(generic.DetailView):
    model = User
    template_name = 'profile/detail.html'
    slug_field = 'username'

