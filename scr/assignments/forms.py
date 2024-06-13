from django import forms

from .models import Assignment, SubmittedAssignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_name', 'description', 'due_date', 'assignment_type', 'file', 'weight', 'max_experience',
                  'damage']


class SubmittedAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubmittedAssignment
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = file.name.split('.')[-1]
            if ext not in ['pdf', 'txt']:
                raise forms.ValidationError('Файл должен быть в формате PDF или TXT.')
        return file
