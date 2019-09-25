from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Profile
from django.conf import settings


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

        labels = {
            'password': "Last 4 digits of a phone number. Or any other passcode or passphrase you like",
            'password2': "Same 4 digits",
            'email': "Email"

        }
        help_texts = {
            'password1': "Your phone? Your church's phone? We will never ask for any sensitive data. So don't stress about remembering a difficult password.",
            'password2': "In case you mistyped it the first time.",
            'email': "So you can receive email notifications or others can contact you."
        }


class ProfileForm(forms.ModelForm):
    org_name = forms.CharField(max_length=100, label='Your church or organization', help_text='Church/Org')
    title = forms.CharField(max_length=50, help_text="Are you a Sunday School teacher? Youth leader? Rector?",
                            label="What's your role?")
    city = forms.CharField(max_length=50, label='City',
                           help_text="So people know a little bit about where you are from.")
    state = forms.CharField(max_length=50, label='State', help_text='State')
    about = forms.CharField(
        max_length=1000,
        label='What else should we know about you?',
        help_text='I am passionate about...',
        widget=forms.Textarea
    )


    class Meta:
        model = Profile
        fields = ('org_name', 'title', 'city', 'state', 'about', 'pic')
