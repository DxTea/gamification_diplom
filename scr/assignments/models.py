import os

from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator

from courses.models import Course
from users.models import CustomUser

from gamification.models import CourseCharacter


class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('homework', 'Домашняя работа'),
        ('theory', 'Теория'),
        ('controlwork', 'Контрольная работа'),
        ('test', 'Тест'),
    ]

    assignment_name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    weight = models.FloatField(null=True, blank=True)
    max_experience = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        default=1
    )
    damage = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        default=1
    )


class SubmittedAssignment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submitted_assignments/')
    submitted_at = models.DateTimeField(auto_now=True)
    submitted_on_time = models.BooleanField(default=True)
    grade = models.IntegerField(null=True, blank=True,
                                validators=[
                                    MaxValueValidator(100),
                                    MinValueValidator(0)
                                ]
                                )
    reviewed = models.BooleanField(default=False)
    experience_gained = models.IntegerField(default=0)
    damage_taken = models.IntegerField(default=0)

    def calculate_experience(self):
        if self.grade:
            self.experience_gained = int(self.assignment.max_experience * int(self.grade) / 100)
            self.save()

    def calculate_damage(self):
        if self.grade == 0:
            self.damage_taken = self.assignment.damage
            course_character = CourseCharacter.objects.get(character=self.student.character,
                                                           course=self.assignment.course)
            course_character.hp -= self.damage_taken
            course_character.save()
        self.save()

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        if self.pk and self.file:
            old_sa = SubmittedAssignment.objects.get(pk=self.pk)
            if old_sa.file and old_sa.file.name != self.file.name:
                if default_storage.exists(old_sa.file.name):
                    default_storage.delete(old_sa.file.name)
        if self.grade:
            self.experience_gained = int(self.assignment.max_experience * int(self.grade) / 100)
            if self.grade == 0:
                self.damage_taken = self.assignment.damage
        super().save(*args, **kwargs)


class TestQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)
    points = models.FloatField(default=100)


class AnswerOption(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='answer_options')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
