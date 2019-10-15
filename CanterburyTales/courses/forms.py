from django import forms
from django_select2.forms import ModelSelect2TagWidget, Select2TagWidget
from CanterburyTales.courses.models import Course, Tag, Profile, CourseFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CourseForm(forms.ModelForm):
    # pseudo_tags = forms.MultipleChoiceField()

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
            'tags': 'Tags'

        }

    course_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', '')
        super(CourseForm, self).__init__(*args, **kwargs)
        self.base_fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('title'),
                                                                  widget=TagsCustomWidget(
                                                                      attrs={"data-token-separators": '[","]'}))


class TagsCustomWidget(Select2TagWidget):
    queryset = Tag.objects.all()

    @property
    def empty_label(self):
        return 'Type in tags'

    def value_from_datadict(self, data, files, name):
        '''Create objects for given non-pimary-key values. Return list of all names as name is the to_field_name.'''
        values = set(super().value_from_datadict(data, files, name))
        # This may only work for Tag, if Tag has title field.
        # You need to implement this method yourself, to ensure proper object creation.
        ids = []
        for val in values:
            if val.isdigit():
                ids.append(val)
            else:
                ids.append(Tag.objects.create(title=val.title()).id)
        return ids


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
