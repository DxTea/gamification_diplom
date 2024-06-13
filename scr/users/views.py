from users.forms import UserRegisterForm, LoginForm
from users.models import CustomUser, Group
from gamification.models import Reward

from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic.edit import FormView


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        group_number = form.cleaned_data.get('group')
        group, created = Group.objects.get_or_create(name=group_number)
        user.group = group
        user.save()
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        rewards = Reward.objects.filter(student=user)
        context['user_profile'] = user
        context['rewards'] = rewards
        context['title'] = f'Профиль пользователя {user}'
        return context


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('users:user_profile', kwargs={'username': self.request.user.username})
