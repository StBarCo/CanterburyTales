from django import forms
from django_select2.forms import Select2MultipleWidget
from CanterburyTales.courses.models import Course, Tag, Profile, CourseFile


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            'title',
            'year_written',
            'tags',
            'audience',
            'count',
            'duration',
            'description',
        ]
        widgets = {
            # 'course_files': forms.FileInput(attrs={'multiple': True})
        }
        labels = {
            'duration': 'Lesson Duration (minutes)',
            'count': 'Number of lessons',


        }

    course_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', '')
        super(CourseForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('title'),
                                                                  widget=Select2MultipleWidget)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'description']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'org_name',
            'city',
            'state',
            'title',
            'about',
            'pic'
        ]
