import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import CustomUser, Group


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    group = forms.CharField(max_length=6, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'group', 'first_name', 'last_name', 'middle_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['middle_name'].required = True
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['email'].label = 'Электронная почта'
        self.fields['role'].label = 'Роль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['middle_name'].label = 'Отчество'
        self.fields['group'].label = 'Группа(номер МЕН)'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        group_number = cleaned_data.get('group')
        if role == 'student' and not re.match(r'^\d{6}$', group_number):
            self.add_error('group', 'Академическая группа должна быть в формате "МЕН-******"')
        else:
            group, created = Group.objects.get_or_create(name=group_number)
            cleaned_data['group'] = group
            print(cleaned_data['group'])
        return cleaned_data
