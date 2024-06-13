from django.db import models
from users.models import CustomUser, Group


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Преподаватель')
    groups = models.ManyToManyField(Group, verbose_name='Группы')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    def total_possible_points(self):
        return sum([assignment.max_experience for assignment in self.assignments.all()])

    def total_points_earned_by_student(self, student):
        return sum([assignment.experience_gained for assignment in
                    student.submittedassignment_set.filter(assignment__course=self)])
