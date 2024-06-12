from django.db import models
from users.models import CustomUser

from courses.models import Course


class Character(models.Model):
    DEFAULT_AVATARS = [
        ('default1.png', 'Default 1'),
        ('default2.png', 'Default 2'),
        ('default3.png', 'Default 3'),
    ]

    name = models.CharField(max_length=255)
    default_avatar = models.CharField(max_length=50, choices=DEFAULT_AVATARS, default='default1.png')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def update_level(self):
        while self.experience >= 100:
            self.level += 1
            self.experience -= 100
            Reward.objects.create(
                student=self.student,
                description=f'Поздравляем! Вы достигли уровня {self.level}!',
                image='level-up.png'
            )
        self.save()


class CourseCharacter(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hp = models.IntegerField(default=100)

    class Meta:
        unique_together = ('character', 'course')


class Reward(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    image = models.CharField(max_length=255)
