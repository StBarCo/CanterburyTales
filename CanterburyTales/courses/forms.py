from django import forms
from django_select2.forms import Select2MultipleWidget
from CanterburyTales.courses.models import Course, Tag, Profile, Audience


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
            'files',

            # 'author',
            # 'posted',
        ]
        widgets = {
            'files': forms.ClearableFileInput(attrs={'multiple': True}),
            # 'author': forms.HiddenInput(),
            # 'posted': forms.HiddenInput(),
            # 'audience': forms.TextInput(),
        }
        labels = {
            'duration': 'Lesson Duration (minutes)',
            'count': 'Number of lessons',


        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', '')
        super(CourseForm, self).__init__(*args, **kwargs)

        self.base_fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('title'),
                                                                  widget=Select2MultipleWidget)
        # self.base_fields['audience'] = forms.IntegerField(
        #     widget=forms.NumberInput(attrs={
        #         'type': 'range',
        #         'data-provide': 'slider',
        #         'data-slider-ticks': list(Audience().get_definitions().keys()),
        #         'data-slider-ticks-labels': list(Audience().get_definitions().values()),
        #         'data-slider-tooltip': 'hide',
        #         'data-slider-lock-to-ticks': '1',
        #         'data-slider-min': '0',
        #         'data-slider-max': '65',
        #         'data-slider-value': '[18, 65]'
        #     })
        # )


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

