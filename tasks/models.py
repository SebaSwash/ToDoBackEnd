from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Modelos para tareas
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.IntegerField()
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    is_obligatory = models.BooleanField()
    notify_at = models.DateTimeField(null=True)
    priority = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    progress = models.FloatField(validators=[
        MinValueValidator(0.0),
        MaxValueValidator(100.0)
    ])

    class Meta:
        db_table = 'Task'


# Modelo para tabla relacional User - Task (tareas asociadas a un usuario)
class UserTask(models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()

    class Meta:
        db_table = 'UserTask'
