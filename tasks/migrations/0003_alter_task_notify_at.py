# Generated by Django 3.2.7 on 2021-09-13 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_usertask_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='notify_at',
            field=models.DateTimeField(null=True),
        ),
    ]
