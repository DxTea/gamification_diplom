from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'groups', 'start_date', 'end_date']
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }
