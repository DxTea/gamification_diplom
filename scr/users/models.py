from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    )

    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, blank=True, null=True, related_name='users')
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=30, blank=False, default='')

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField('CustomUser', limit_choices_to={'role': 'student'}, related_name='student_groups')

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name
