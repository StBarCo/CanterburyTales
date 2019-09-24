from django import forms
from django_select2.forms import Select2MultipleWidget
from CanterburyTales.courses.models import Course, Audience, Tag, Profile


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'year_written',
            'tags',
            'audience',
            'lesson_length',
            'description',
            # 'author',
            # 'posted',
        ]
        widgets = {
            # 'author': forms.HiddenInput(),
            # 'posted': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', '')
        super(CourseForm, self).__init__(*args, **kwargs)

        self.base_fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('title'),
                                                                  widget=Select2MultipleWidget)
        self.base_fields['audience'] = forms.ModelMultipleChoiceField(queryset=Audience.objects.all(),
                                                                      widget=Select2MultipleWidget)


class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['title', 'description']


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
