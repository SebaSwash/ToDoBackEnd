# Generated by Django 3.2.7 on 2021-10-22 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_notify_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='end_time',
            new_name='deadline',
        ),
    ]
