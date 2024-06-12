# Generated by Django 5.0.6 on 2024-06-12 06:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0013_alter_assignment_assignment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='damage',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='assignment',
            name='max_experience',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='submittedassignment',
            name='damage_taken',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='submittedassignment',
            name='experience_gained',
            field=models.IntegerField(default=0),
        ),
    ]