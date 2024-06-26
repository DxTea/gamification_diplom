# Generated by Django 5.0.6 on 2024-06-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='default_avatar',
            field=models.CharField(choices=[('default1.png', 'Default 1'), ('default2.png', 'Default 2'), ('default3.png', 'Default 3')], default='default1.png', max_length=50),
        ),
        migrations.AlterField(
            model_name='character',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
