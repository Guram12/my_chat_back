# Generated by Django 5.0.6 on 2024-05-29 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_customuser_last_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
