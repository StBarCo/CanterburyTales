from django.contrib import admin

from .models import Course, Profile, Tag


admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Tag)
