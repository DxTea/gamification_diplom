from django import forms
from .models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'default_avatar', 'avatar']
        labels = {
            'name': 'Имя',
            'level': 'Уровень',
            'experience': 'Опыт',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False
