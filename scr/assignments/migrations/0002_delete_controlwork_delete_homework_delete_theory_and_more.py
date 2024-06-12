# Generated by Django 5.0.6 on 2024-05-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ControlWork',
        ),
        migrations.DeleteModel(
            name='Homework',
        ),
        migrations.DeleteModel(
            name='Theory',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='object_id',
        ),
        migrations.AddField(
            model_name='assignment',
            name='assignment_type',
            field=models.CharField(
                choices=[('homework', 'Домашняя работа'), ('theory', 'Теория'), ('controlwork', 'Контрольная работа')],
                default='homework', max_length=20),
            preserve_default=False,
        ),
    ]
